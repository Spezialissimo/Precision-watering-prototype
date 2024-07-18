import csv
from dotenv import dotenv_values
from datetime import datetime
import os
import time

# filepath = "repository/" + dotenv_values(".env")["DATA_FILE"]
filepath = "/home/spezialissimo/Documents/tesi/arduino/small_watering/dashboard/repository/data.csv"

def format_sensor_data(data):# Create a dictionary for the formatted data
    formatted_data = {"timestamp": data["timestamp"]}
    for item in data['data']:
        key = f"v_{item['x']}_{item['y']}"
        formatted_data[key] = item['v']


    expected_keys = [
        f"v_{x}_{y}" for x in [10, 15, 20, 25, 30] for y in [5, 10, 15, 20, 25]
    ]
    for key in expected_keys:
        if key not in formatted_data:
            formatted_data[key] = None

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
    formatted_data = format_sensor_data(data)
    file_exists = os.path.exists(filepath)

    with open(filepath, mode='a', newline='') as file:
        fieldnames = ["timestamp"] + [
            f"v_{x}_{y}" for x in [10, 15, 20, 25, 30] for y in [5, 10, 15, 20, 25]
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(formatted_data)


def get_last_sensor_data(interpolate=False):
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if rows:
                if interpolate:
                    return parse_sensor_data(rows[-1])
                return parse_sensor_data(filter_interpolated_data(rows[-1]))
            else:
                return None
    except FileNotFoundError:
        return None

def filter_interpolated_data(data):
    needed_keys = [
        f"v_{x}_{y}" for x in [10,  30] for y in [5, 15, 25]
    ]
    needed_keys.append("timestamp")

    return {key: data[key] for key in needed_keys}


def get_all_sensor_data(seconds=None):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            all_data = [parse_sensor_data(filter_interpolated_data(row)) for row in reader]

            if seconds is not None:
                current_time = time.time()
                return [data for data in all_data if current_time - float(data["timestamp"]) <= seconds]

            return all_data
    except FileNotFoundError:
        return []