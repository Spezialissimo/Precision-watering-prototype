import csv
from dotenv import dotenv_values
from datetime import datetime
import os
import time
import threading

filepath = "repository/" + dotenv_values(".env")["DATA_FILE"]
last_sensor_value = {}
lock = threading.Lock()

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
            x = int(parts[1])
            y = int(parts[2])
            v = int(value)
            data.append({'x': x, 'y': y, 'v': v})
    return {'timestamp': timestamp, 'data': data}

def save_sensor_data(data):
    global last_sensor_value
    lock.acquire()
    last_sensor_value = data
    lock.release()
    formatted_data = format_sensor_data(data)
    file_exists = os.path.exists(filepath)

    with open(filepath, mode='a', newline='') as file:
        fieldnames = list(formatted_data.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(formatted_data)


def get_last_sensor_data(interpolate=False):
    global last_sensor_value
    result = {}
    lock.acquire()
    result = last_sensor_value

    if(result == {}):
        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, mode='r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    if interpolate:
                        result = parse_sensor_data(rows[-1])
                    result = filter_interpolated_data(parse_sensor_data(rows[-1]))
                else:
                    return None
        except FileNotFoundError:
            return None
    if not interpolate:
        result = filter_interpolated_data(result)
    lock.release()
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
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            all_data = [filter_interpolated_data(parse_sensor_data((row))) for row in reader]

            if seconds is not None:
                current_time = time.time()
                return [data for data in all_data if current_time - float(data["timestamp"]) <= seconds]

            return all_data
    except FileNotFoundError:
        return []