from flask import jsonify, render_template, request
from . import app
from moisture_system.moisture_system import togglePump, set_moisture
from repository.data import get_last_sensor_data, get_all_sensor_data, get_last_irrigation_data, get_all_irrigation_data

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

@app.route('/getIrrigationHistoryData', methods=['GET'])
def get_irrigation_history_data():
    seconds = request.args.get('seconds', default=None, type=int)
    if seconds is None:
        sensor_data = get_all_irrigation_data()
    else:
        sensor_data = get_all_irrigation_data(seconds)
    return jsonify(sensor_data)

@app.route('/getIrrigationData', methods=['GET'])
def get_irrigation_data():
    return jsonify(get_last_irrigation_data())

@app.route('/setIrrigation', methods=['POST'])
def set_irrigation():
    value = request.args.get('value', default=None, type=int)
    set_moisture(value)
    return jsonify({"value": value})

def start_flask(host, port):
    app.run(host=host, port=port, debug=False)
