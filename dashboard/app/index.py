from flask import jsonify, render_template
from . import app
from moisture_system.moisture_system import togglePump
from repository.data import get_last_sensor_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getLastReadings', methods=['GET'])
def get_data():
    return jsonify(get_last_sensor_data())

@app.route('/getHistory', methods=['GET'])
def get_history():
    pass

@app.route('/togglePump', methods=['GET'])
def toggle_pump():
    pump_state = togglePump()
    return jsonify({"pump_state": pump_state})


def start_flask(host, port):
    app.run(host=host, port=port, debug=False)
