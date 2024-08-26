from flask import jsonify, render_template, request, Response, send_from_directory
from flask_socketio import send
from . import router
from . import socketio
import time
import threading

dc = None

@router.route('/')
def index():
    return render_template('index.html')

@router.route('/sensors/interpolated', methods=['GET'])
def get_last_sensor_data_with_interpolation():
    return jsonify(dc.get_last_sensor_data_with_interpolation())

@router.route('/sensors/', methods=['GET'])
def get_last_sensor_data():
    return jsonify(dc.get_last_sensor_data())

@router.route('/irrigation/history', methods=['GET'])
def get_history_irrigation_data():
    seconds = request.args.get('seconds', default=None, type=int)
    return jsonify(dc.get_all_irrigation_data(seconds))

@router.route('/irrigation/', methods=['GET'])
def get_last_irrigation_data():
    return jsonify(dc.get_last_irrigation_data())

@router.route('/irrigation/slider', methods=['POST'])
def set_irrigation_value():
    value = request.args.get('value', default=None, type=int)
    dc.set_new_optimal_value(value)
    return Response(status=200)

@router.route('/irrigation/matrix', methods=['POST'])
def set_irrigation_matrix():
    matrixId = request.args.get('matrix', default=None, type=str)
    dc.set_new_optimal_matrix(matrixId)
    avarage = dc.get_optimal_matrix_average()
    return jsonify(avarage)

@router.route('/irrigation/mode', methods=['POST'])
def set_irrigation_mode():
    mode = request.args.get('mode', default=None, type=str)
    dc.set_irrigation_mode(mode)
    return Response(status=200)

@router.route('/pump/', methods=['POST'])
def set_pump_state():
    dc.toggle_pump()
    return Response(status=200)

@router.route('/irrigation/optimal/', methods=['GET'])
def get_optimals():
    return jsonify(dc.get_optimals())

@router.route('/irrigation/optimal/image/<imageId>', methods=['GET'])
def get_optimal_matrix_image(imageId):
    return send_from_directory('../assets', imageId + '.png')

def send_pump_state():
    while True:
        pump_state = dc.get_pump_state()
        socketio.emit('pump_state_update', {'pump_state': pump_state.name})
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    thread = threading.Thread(target=send_pump_state)
    thread.start()

def start_flask(host, port, data_collector):
    global dc
    dc = data_collector
    socketio.run(router, host=host, port=port, debug=False)
