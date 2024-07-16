import serial
from datetime import datetime
import pytz
import json
from flask import Flask, jsonify, render_template
import numpy as np
from scipy.interpolate import interpn
from threading import Thread

app = Flask(__name__)

# Configuration variables
host = '127.0.0.1'
port = 5001
SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600
tz = pytz.timezone("Europe/Rome")

# Global variables
last_moisture_values = {}
pump_state = False

# Grid points for interpolation
x_values = [10, 30]
y_values = [5, 15, 25]
points = np.array([[x, y] for x in x_values for y in y_values])

# Serial port setup
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getLastReadings', methods=['GET'])
def get_data():
    global last_moisture_values
    return jsonify(last_moisture_values)

@app.route('/togglePump', methods=['GET'])
def toggle_pump():
    global pump_state
    pump_state = not pump_state
    ser.write(b"1" if pump_state else b"0")
    return jsonify({"pump_state": pump_state})

def receiving(ser):
    print("Receiving thread started")
    global last_moisture_values
    global points
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
                xi = np.array([
                    [10, 10], [10, 20],
                    [15, 5], [15, 10], [15, 15], [15, 20], [15, 25],
                    [20, 5], [20, 10], [20, 15], [20, 20], [20, 25],
                    [25, 5], [25, 10], [25, 15], [25, 20], [25, 25],
                    [30, 10], [30, 20]
                ])
                interpolated_values = interpn((x_values, y_values), values_grid, xi)
                new_data = []
                for i, point in enumerate(xi):
                    new_data.append({
                        "x": int(point[0]),
                        "y": int(point[1]),
                        "v": int(interpolated_values[i])
                    })
                data["data"].extend(new_data)
                data["timestamp"] = datetime.now().timestamp()
                last_moisture_values = data
        except Exception as e:
            print("Error receiving data:", e)

def start_flask(host, port):
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    # Start receiving thread for serial data
    receiving_thread = Thread(target=receiving, args=(ser,))
    receiving_thread.start()

    # Start Flask app in a separate thread
    flask_thread = Thread(target=start_flask, args=(host, port))
    flask_thread.start()
