import serial
from datetime import datetime
import pytz
from time import sleep
import json
from flask import Flask, jsonify, render_template, request
import random
from threading import Thread

app = Flask(__name__)

host = '127.0.0.1'
port = 5001
last_moisture_values = {}

tz = pytz.timezone("Europe/Rome")

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600
DEMO = False

ser = ""

if ( DEMO != True ):
    ser =serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getLastReadings', methods=['GET'])
def get_data():
    global last_moisture_values
    moisture_values = {}
    if( DEMO ):
        moisture_values = {
            "timestamp": datetime.now().timestamp(),
            "ms_10_10": random.randint(0, 100),
            "ms_10_30": random.randint(0, 100),
            "ms_20_10": random.randint(0, 100),
            "ms_20_30": random.randint(0, 100),
            "ms_30_10": random.randint(0, 100),
            "ms_30_30": random.randint(0, 100)
        }
    if( last_moisture_values != {}):
        moisture_values = moisture_values = {
            key: min(int(value), 100) if key != "timestamp" else value
            for key, value in last_moisture_values.items()
        }


    return jsonify(moisture_values)

def receiving(ser):
    print("Receiving thread started")
    global last_moisture_values
    buffer = ''

    while True:
        bytes_to_read = ser.inWaiting()
        if bytes_to_read > 0:
            buffer += ser.read(bytes_to_read).decode('utf-8')

        if '\n' in buffer:
            lines = buffer.split('\n')
            last_received = lines[-2]
            buffer = lines[-1]
            try:
                last_moisture_values = json.loads(last_received)
                last_moisture_values["timestamp"] = datetime.now().timestamp()
            except:
                print("Error parsing json")

def start_flask(host, port):
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    if( DEMO != True ):
        Thread(target=receiving, args=(ser,)).start()
    Thread(target=start_flask, args = (host, port)).start()

