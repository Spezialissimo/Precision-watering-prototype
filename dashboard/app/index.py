from flask import jsonify, render_template, request
from . import app
from moisture_system.moisture_system import togglePump
from repository.data import get_last_sensor_data, get_all_sensor_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getLastReadingsWithInterpolation', methods=['GET'])
def get_data():
    return jsonify(get_last_sensor_data(interpolate=True))

@app.route('/getLastReadings', methods=['GET'])
def get_last_data():
    return jsonify(get_last_sensor_data())


@app.route('/getHistory', methods=['GET'])
def get_history():
    seconds = request.args.get('seconds', default=None, type=int)
    sensor_data = get_all_sensor_data(seconds)
    return jsonify(sensor_data)

@app.route('/togglePump', methods=['GET'])
def toggle_pump():
    pump_state = togglePump()
    return jsonify({"pump_state": pump_state})

def start_flask(host, port):
    app.run(host=host, port=port, debug=False)
