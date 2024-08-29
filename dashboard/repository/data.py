import csv
from dotenv import load_dotenv
import os
import threading
import time

load_dotenv()

irrigation_file = os.getenv("IRRIGATION_FILE", "default_file.csv")
irrigation_check_period = int(os.getenv("IRRIGATION_CHECK_PERIOD", 60))

base_dir = os.path.dirname(os.path.abspath(__file__))
__irrigation_filepath = os.path.normpath(os.path.join(base_dir, '..', 'repository', irrigation_file))
__irrigation_check_period = irrigation_check_period
__lock_last_irrigation_value = threading.Lock()
__lock_irrigation_file = threading.Lock()
__last_irrigation_value = {}

def read_last_lines(file_path, num_lines):
    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        buffer_size = 1024
        buffer = bytearray()
        lines = []
        end_position = file_size

        while end_position > 0 and len(lines) <= num_lines:
            start_position = max(0, end_position - buffer_size)
            file.seek(start_position)
            buffer[0:(end_position - start_position)] = file.read(end_position - start_position)
            lines = buffer.decode().splitlines()
            end_position = start_position

    return lines[-num_lines:]

def file_is_empty():
    return os.stat(__irrigation_filepath).st_size == 0

def __last_is_too_old(data = { 'timestamp': time.time() }):
    try:
        last_line = read_last_lines(__irrigation_filepath, 1)
        if last_line and len(last_line) == 1 and "timestamp" not in last_line[0] and  last_line[0] != "":
            last_timestamp = float(last_line[0].split(',')[0])
            current_timestamp = float(data['timestamp'])
            if current_timestamp - last_timestamp >= ((__irrigation_check_period * 3)):
                return True
        return not last_line
    except:
        return True

def save_irrigation_data(data):
    global __last_irrigation_value
    file_exists = os.path.exists(__irrigation_filepath)

    if not __last_irrigation_value:
        if file_exists:
            last_lines = read_last_lines(__irrigation_filepath, 1)
            if last_lines and len(last_lines) == 1 and "timestamp" in last_lines[0]:
                __last_irrigation_value = parse_irrigation_data(next(csv.DictReader(last_lines), {}))

    with __lock_last_irrigation_value:
        __last_irrigation_value = data

    clear_file = False

    if file_exists:
        if __last_is_too_old(data):
            clear_file = True

    with __lock_irrigation_file:
        mode = 'w' if clear_file else 'a'
        with open(__irrigation_filepath, mode=mode, newline='') as file:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if clear_file or not file_exists or file_is_empty():
                writer.writeheader()

            writer.writerow(data)

def parse_irrigation_data(row):
    new_dict = {}
    for key, value in row.items():
        try:
            new_dict[key] = float(value)
        except:
            return None
    return new_dict

def should_restore_backup():
    file_exists = os.path.exists(__irrigation_filepath)
    if file_exists:
        return not __last_is_too_old()
    return False

def get_all_irrigation_data(seconds=None):
    try:
        if not os.path.exists(__irrigation_filepath):
            return []

        avg_line_interval = 15
        num_lines = (seconds // avg_line_interval) + 1 if seconds else 100

        with __lock_irrigation_file:
            lines = read_last_lines(__irrigation_filepath, num_lines)

        if not lines:
            return []

        reader = csv.DictReader(lines)
        raw_data = list(reader)

        result = []

        if seconds is not None:
            end_time = time.time()
            start_time = end_time - seconds

            for row in raw_data:
                if start_time <= float(row["timestamp"]) <= end_time:
                    value = parse_irrigation_data(row)
                    if value is None:
                        reset_file()
                    else:
                        result.append(parse_irrigation_data(row))
        else:
            for row in raw_data:
                value = parse_irrigation_data(row)
                if value is None:
                    reset_file()
                    break
                else:
                    result.append(parse_irrigation_data(row))
        return result
    except:
        return []

def reset_file():
    with __lock_irrigation_file:
        mode = 'w'
        with open(__irrigation_filepath, mode=mode, newline='') as file:
            fieldnames = list(["timestamp", "r", "irrigation", "optimal_m", "current_m"])
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()