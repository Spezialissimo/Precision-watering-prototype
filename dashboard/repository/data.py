import csv
from dotenv import dotenv_values
import os
import time
import threading
from collections import defaultdict

sensors_filepath = "repository/" + dotenv_values(".env")["DATA_FILE"]
irrigation_filepath = "repository/" + dotenv_values(".env")["IRRIGATION_FILE"]
last_sensor_value = {}
last_irrigation_value = { "timestamp": 0, "r": 0, "irrigation": 0, "optimal_m": 0, "current_m": 0 }
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
            x = int(parts[1])
            y = int(parts[2])
            v = int(value)
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


def get_all_sensor_data(seconds=None, aggregation_interval=10):
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

        if aggregation_interval is not None:
            return aggregate_sensor_data(all_data, aggregation_interval)
        return all_data

    else:
        all_data = [filter_interpolated_data(parse_sensor_data(row)) for row in raw_data]

        if aggregation_interval is not None:
            return aggregate_sensor_data(all_data, aggregation_interval)
        return all_data


def aggregate_sensor_data(data, interval):
    if not data:
        return []

    # Convert timestamp to float and sort data by timestamp
    for entry in data:
        entry["timestamp"] = float(entry["timestamp"])

    data.sort(key=lambda x: x["timestamp"])

    aggregated_data = []
    interval_data = defaultdict(lambda: defaultdict(lambda: {'sum': 0, 'count': 0}))

    start_time = data[0]["timestamp"]
    end_time = start_time + interval

    for entry in data:
        timestamp = entry["timestamp"]
        if timestamp < end_time:
            for key, value in entry.items():
                if key != "timestamp":
                    if isinstance(value, list):  # Check if value is a list of dicts
                        for item in value:
                            # Extract the 'x', 'y', and 'v' fields from each dictionary
                            x, y, v = item['x'], item['y'], item['v']
                            interval_data[(x, y)][end_time]['sum'] += float(v)
                            interval_data[(x, y)][end_time]['count'] += 1
        else:
            # Process the current interval
            interval_aggregated_data = []
            for (x, y), stats in interval_data.items():
                for time_key, values in stats.items():
                    if values['count'] > 0:
                        avg_v = values['sum'] / values['count']
                        interval_aggregated_data.append({'x': x, 'y': y, 'v': avg_v})
            aggregated_data.append({'timestamp': start_time, 'data': interval_aggregated_data})

            # Move to the next interval
            start_time = end_time
            end_time = start_time + interval
            interval_data = defaultdict(lambda: defaultdict(lambda: {'sum': 0, 'count': 0}))

            # Add the current entry to the new interval
            for key, value in entry.items():
                if key != "timestamp":
                    if isinstance(value, list):
                        for item in value:
                            x, y, v = item['x'], item['y'], item['v']
                            interval_data[(x, y)][end_time]['sum'] += float(v)
                            interval_data[(x, y)][end_time]['count'] += 1

    # Append the last interval data if available
    interval_aggregated_data = []
    for (x, y), stats in interval_data.items():
        for time_key, values in stats.items():
            if values['count'] > 0:
                avg_v = values['sum'] / values['count']
                interval_aggregated_data.append({'x': x, 'y': y, 'v': avg_v})
    aggregated_data.append({'timestamp': start_time, 'data': interval_aggregated_data})

    return aggregated_data



def save_irrigation_data(data):
    global last_irrigation_value
    lock_last_irrigation_value.acquire()
    last_irrigation_value = data
    lock_last_irrigation_value.release()
    file_exists = os.path.exists(irrigation_filepath)
    lock_irrigation_file.acquire()
    with open(irrigation_filepath, mode='a', newline='') as file:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)


        if not file_exists:
            writer.writeheader()

        writer.writerow(data)
    lock_irrigation_file.release()

def get_last_irrigation_data():
    global last_irrigation_value
    result = {}
    lock_last_irrigation_value.acquire()
    result = last_irrigation_value
    lock_last_irrigation_value.release()

    if(result == {}):
        if not os.path.exists(irrigation_filepath):
            return None

        try:
            with open(irrigation_filepath, mode='r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    result = rows[-1]
                else:
                    return None
        except FileNotFoundError:
            return None
    return result

def get_all_irrigation_data(seconds=None, aggregation_interval=None):
    if not os.path.exists(irrigation_filepath):
        return []

    try:
        lock_irrigation_file.acquire()
        with open(irrigation_filepath, mode='r') as file:
            reader = csv.DictReader(file)
            if seconds is not None:
                end_time = time.time()
                start_time = end_time - seconds
                all_data = []
                for row in reader:
                    timestamp = float(row["timestamp"])
                    if timestamp >= start_time:
                        all_data.append(row)
                    if timestamp > end_time:
                        break
                if aggregation_interval is not None:
                    lock_irrigation_file.release()
                    return aggregate_data(all_data, aggregation_interval)
                lock_irrigation_file.release()
                return all_data
            else:
                all_data = [row for row in reader]
                if aggregation_interval is not None:
                    lock_irrigation_file.release()
                    return aggregate_data(all_data, aggregation_interval)
                lock_irrigation_file.release()
                return all_data

    except FileNotFoundError:
        lock_irrigation_file.release()
        return []

def aggregate_data(data, interval):
    if not data:
        return []

    # Convert timestamp to float and sort data by timestamp
    for entry in data:
        entry["timestamp"] = float(entry["timestamp"])
    data.sort(key=lambda x: x["timestamp"])

    aggregated_data = []
    interval_data = defaultdict(lambda: {'current_m': 0, 'optimal_m': 0, 'count': 0})

    start_time = data[0]["timestamp"]
    end_time = start_time + interval

    for entry in data:
        timestamp = entry["timestamp"]
        if timestamp < end_time:
            interval_data[end_time]['current_m'] += float(entry["current_m"])
            interval_data[end_time]['optimal_m'] += float(entry["optimal_m"])
            interval_data[end_time]['count'] += 1
        else:
            # Process the current interval
            if interval_data[end_time]['count'] > 0:
                aggregated_data.append({
                    "timestamp": start_time,
                    "current_m": interval_data[end_time]['current_m'] / interval_data[end_time]['count'],
                    "optimal_m": interval_data[end_time]['optimal_m'] / interval_data[end_time]['count']
                })
            # Move to the next interval
            start_time = end_time
            end_time = start_time + interval
            interval_data[end_time]['current_m'] = float(entry["current_m"])
            interval_data[end_time]['optimal_m'] = float(entry["optimal_m"])
            interval_data[end_time]['count'] = 1

    # Append the last interval data if available
    if interval_data[end_time]['count'] > 0:
        aggregated_data.append({
            "timestamp": start_time,
            "current_m": interval_data[end_time]['current_m'] / interval_data[end_time]['count'],
            "optimal_m": interval_data[end_time]['optimal_m'] / interval_data[end_time]['count']
        })

    return aggregated_data