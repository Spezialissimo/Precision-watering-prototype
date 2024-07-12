import serial
from datetime import datetime
import pytz
from time import sleep
import json
from flask import Flask, jsonify, render_template, request
import requests
from threading import Thread

app = Flask(__name__)

host = '127.0.0.1'
port = 5000
last_received = ''

tz = pytz.timezone("Europe/Rome")

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600

ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getLastReadings', methods=['GET'])
def get_data():
    print(last_received)
    moisture_values = {}
    if( last_received != ""):
        try:
            moisture_values = json.loads(last_received)
            print(json.dumps(moisture_values, indent=4))
        except:
            print("Error parsing json")
    return jsonify(moisture_values)

def receiving(ser):
    print("Receiving thread started")
    global last_received
    buffer = ''

    while True:
        bytes_to_read = ser.inWaiting()
        if bytes_to_read > 0:
            buffer += ser.read(bytes_to_read).decode('utf-8')

        if '\n' in buffer:
            lines = buffer.split('\n')
            last_received = lines[-2]
            buffer = lines[-1]

def start_flask(host, port):
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    Thread(target=receiving, args=(ser,)).start()
    Thread(target=start_flask, args = (host, port)).start()

