import csv
from dotenv import dotenv_values
import os
import time
import threading
from datetime import datetime

sensors_filepath = os.path.normpath("repository/" + dotenv_values(".env")["DATA_FILE"])
irrigation_filepath = os.path.normpath("repository/" + dotenv_values(".env")["IRRIGATION_FILE"])
last_sensor_value = {}
last_irrigation_value = {}
lock_last_sensor_value = threading.Lock()
lock_last_irrigation_value = threading.Lock()
lock_sensor_file = threading.Lock()
lock_irrigation_file = threading.Lock()

def format_sensor_data(data):
    formatted_data = {"timestamp": data["timestamp"]}
    for item in data['data']:
        key = f"v_{item['x']}_{item['y']}"
        formatted_data[key] = item['v']

    return formatted_data

def parse_sensor_data(row):
    timestamp = row['timestamp']
    data = []
    for key, value in row.items():
        if key != 'timestamp' and value:
            parts = key.split('_')
            x = float(parts[1])
            y = float(parts[2])
            v = float(value)
            data.append({'x': x, 'y': y, 'v': v})
    return {'timestamp': timestamp, 'data': data}

def save_sensor_data(data):
    global last_sensor_value
    lock_last_sensor_value.acquire()
    last_sensor_value = data
    lock_last_sensor_value.release()
    formatted_data = format_sensor_data(data)
    file_exists = os.path.exists(sensors_filepath)

    lock_sensor_file.acquire()
    with open(sensors_filepath, mode='a', newline='') as file:
        fieldnames = list(formatted_data.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(formatted_data)
    lock_sensor_file.release()



def get_last_sensor_data(interpolate=False):
    global last_sensor_value
    result = {}
    lock_last_sensor_value.acquire()
    result = last_sensor_value
    lock_last_sensor_value.release()
    if result != {} :
        if not interpolate:
            result = filter_interpolated_data(result)
    return result

def filter_interpolated_data(data):
    result = {
        "timestamp": data["timestamp"],
        "data": []
    }
    for value in data["data"]:
        if value["x"]  in [10, 30] and value["y"] in [5, 15, 25]:
            result['data'].append(value)
    return result


def get_all_sensor_data(seconds=None):
    if not os.path.exists(sensors_filepath):
        return []

    try:
        lock_sensor_file.acquire()
        with open(sensors_filepath, mode='r') as file:
            reader = csv.DictReader(file)
            raw_data = list(reader)  # Leggi tutti i dati una volta

    except FileNotFoundError:
        return []

    finally:
        lock_sensor_file.release()  # Rilascia il lock subito dopo la lettura

    all_data = []

    if seconds is not None:
        current_time = time.time()
        start_time = current_time - seconds
        for row in raw_data:
            timestamp = float(row["timestamp"])
            if timestamp >= start_time:
                processed_row = filter_interpolated_data(parse_sensor_data(row))
                all_data.append(processed_row)
            if timestamp > current_time:
                break

        return all_data

    else:
        all_data = [filter_interpolated_data(parse_sensor_data(row)) for row in raw_data]
        return all_data


def save_irrigation_data(data):
    global last_irrigation_value

    # Aggiorna last_irrigation_value con lock
    lock_last_irrigation_value.acquire()
    last_irrigation_value = data
    lock_last_irrigation_value.release()

    file_exists = os.path.exists(irrigation_filepath)

    # Scrivi nel file con lock
    lock_irrigation_file.acquire()
    try:
        with open(irrigation_filepath, mode='a', newline='') as file:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)
    finally:
        lock_irrigation_file.release()

def parse_irrigation_data(row):
    new_dict = {}
    for key, value in row.items():
        try:
            new_dict[key] = float(value)
        except ValueError:
            new_dict[key] = value
    return new_dict

def get_last_irrigation_data():
    global last_irrigation_value
    result = {}

    lock_last_irrigation_value.acquire()
    result = last_irrigation_value
    lock_last_irrigation_value.release()

    if result == {}:
        # Leggi il file con lock
        lock_irrigation_file.acquire()
        try:
            with open(irrigation_filepath, mode='r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    result = rows[-1]
        except FileNotFoundError:
            lock_irrigation_file.release()
            save_irrigation_data({'timestamp': datetime.now().timestamp(), 'r': 0, 'irrigation': 10, 'optimal_m': 50, 'current_m': 0})
        finally:
            if lock_irrigation_file.locked():
                lock_irrigation_file.release()
            lock_last_irrigation_value.acquire()
            last_irrigation_value = result
            lock_last_irrigation_value.release()
    if(result == {}):
        return get_last_irrigation_data()
    return parse_irrigation_data(result)


def get_all_irrigation_data(seconds=None, aggregation_interval=None):
    if not os.path.exists(irrigation_filepath):
        return []

    # Leggi il file con lock
    lock_irrigation_file.acquire()
    try:
        with open(irrigation_filepath, mode='r') as file:
            reader = csv.DictReader(file)
            raw_data = list(reader)
    except FileNotFoundError:
        return []
    finally:
        lock_irrigation_file.release()

    if seconds is not None:
        end_time = time.time()
        start_time = end_time - seconds
        all_data = [row for row in raw_data if start_time <= float(row["timestamp"]) <= end_time]
        result = []
        for row in all_data:
            result.append(parse_irrigation_data(row))
        return result
    else:
        all_data = raw_data
        result = []
        for row in all_data:
            result.append(parse_irrigation_data(row))
        return result
