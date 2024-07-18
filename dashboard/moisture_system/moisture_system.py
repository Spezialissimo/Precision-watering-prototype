import serial
from datetime import datetime
import pytz
import json
import numpy as np
from scipy.interpolate import interpn
import threading
from repository.data import save_sensor_data
from dotenv import dotenv_values

tz = pytz.timezone("Europe/Rome")
pump_state = False
lock = threading.Lock()
ser = serial.Serial(dotenv_values(".env")["SERIAL_PORT"], int(dotenv_values(".env")["SERIAL_BAUDRATE"]), timeout=1)

def togglePump():
    global pump_state
    pump_state = not pump_state
    ser.write(b"1" if pump_state else b"0")
    return pump_state

def receive(serial_port, baudrate):
    x_values = [10, 30]
    y_values = [5, 15, 25]
    points = np.array([[x, y] for x in x_values for y in y_values])

    buffer = ''

    while True:
        try:
            bytes_to_read = ser.inWaiting()
            if bytes_to_read > 0:
                buffer += ser.read(bytes_to_read).decode('utf-8')

            if '\n' in buffer:
                lines = buffer.split('\n')
                last_received = lines[-2]
                buffer = lines[-1]
                data = json.loads(last_received)
                values = data["data"]
                formatted_values = []
                for point in points:
                    found = False
                    for value in values:
                        if value["x"] == point[0] and value["y"] == point[1]:
                            formatted_values.append(value["v"])
                            found = True
                            break
                    if not found:
                        formatted_values.append(0)
                values_grid = np.array(formatted_values).reshape((len(np.unique(points[:,0])), len(np.unique(points[:,1]))))
                x_range = np.arange(10, 31, 1)  # Da 10 a 30 cm ogni 1 cm
                y_range = np.arange(5, 26, 1)   # Da 5 a 25 cm ogni 1 cm
                x_grid, y_grid = np.meshgrid(x_range, y_range)
                xi = np.vstack([x_grid.ravel(), y_grid.ravel()]).T
                interpolated_values = interpn((x_values, y_values), values_grid, xi)
                new_data = []
                for i, point in enumerate(xi):
                    new_data.append({
                        "x": int(point[0]),
                        "y": int(point[1]),
                        "v": int(interpolated_values[i])
                    })
                data["data"] = new_data
                data["timestamp"] = datetime.now().timestamp()
                with lock:
                    save_sensor_data(data)
        except Exception as e:
            print("Error receiving data:", e)
