from flask import session, jsonify, render_template, request, Response, send_from_directory, redirect, Flask
from threading import Thread
from uuid import uuid4
from controller.controller import Controller
import os
from datetime import datetime
router = Flask(__name__)

user_simulations = {}
router.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

def start_simulation_for_user():
    user_id = session.get('user_id')

    if not user_id:
        user_id = str(uuid4())
        session['user_id'] = user_id

        controller = Controller()
        user_simulations[user_id] = {
            'controller': controller,
            'threads': []
        }

        sensor_thread = Thread(target=controller.receive_sensor_data_thread)
        sensor_thread.start()

        irrigation_thread = Thread(target=controller.compute_irrigation_thread)
        irrigation_thread.start()

        user_simulations[user_id]['threads'].extend([sensor_thread, irrigation_thread])

@router.route('/')
def index():
    session.clear()
    start_simulation_for_user()
    controller = user_simulations[session['user_id']]['controller']
    ip = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    server_ip = f"http://{ip}:{port}"
    moisture_scale_min = int(os.getenv("MOISTURE_IN_FRONTEND_MIN", 0))
    moisture_scale_max = int(os.getenv("MOISTURE_IN_FRONTEND_MAX", 100))
    timestamp = datetime.now().timestamp()
    return render_template('index.html', server_ip=server_ip, moisture_scale_min=moisture_scale_min, moisture_scale_max=moisture_scale_max, timestamp=timestamp)

@router.route('/sensors/interpolated', methods=['GET'])
def get_last_sensor_data_with_interpolation():
    controller = user_simulations[session['user_id']]['controller']
    return jsonify(controller.get_last_sensor_data_with_interpolation())

@router.route('/sensors/', methods=['GET'])
def get_last_sensor_data():
    controller = user_simulations[session['user_id']]['controller']
    return jsonify(controller.get_last_sensor_data())

@router.route('/irrigation/history', methods=['GET'])
def get_history_irrigation_data():
    controller = user_simulations[session['user_id']]['controller']
    seconds = request.args.get('seconds', default=None, type=int)
    return jsonify([controller.get_last_irrigation_data()])

@router.route('/irrigation/', methods=['GET'])
def get_last_irrigation_data():
    controller = user_simulations[session['user_id']]['controller']
    return jsonify(controller.get_last_irrigation_data())

@router.route('/irrigation/slider', methods=['POST'])
def set_irrigation_value():
    controller = user_simulations[session['user_id']]['controller']
    value = request.args.get('value', default=None, type=float)
    controller.set_new_optimal_value(value)
    return Response(status=200)

@router.route('/irrigation/matrix', methods=['POST'])
def set_irrigation_matrix():
    controller = user_simulations[session['user_id']]['controller']
    data = request.get_json()
    matrix = data.get('matrix', None)
    controller.set_new_optimal_matrix(matrix)
    average = controller.get_optimal_matrix_average()
    return jsonify(average)

@router.route('/irrigation/mode', methods=['POST'])
def set_irrigation_mode():
    controller = user_simulations[session['user_id']]['controller']
    mode = request.args.get('mode', default=None, type=str)
    controller.set_irrigation_mode(mode)
    return Response(status=200)

@router.route('/pump/', methods=['POST'])
def set_pump_state():
    controller = user_simulations[session['user_id']]['controller']
    controller.toggle_pump()
    pump_state = controller.get_pump_state()
    return jsonify(pump_state.name)

@router.route('/pump/state', methods=['GET'])
def get_pump_state():
    controller = user_simulations[session['user_id']]['controller']
    pump_state = controller.get_pump_state()
    return jsonify(pump_state.name)

@router.route('/irrigation/optimal/', methods=['GET'])
def get_optimals():
    controller = user_simulations[session['user_id']]['controller']
    return jsonify(controller.get_optimals())

@router.route('/irrigation/optimal/image/<imageId>', methods=['GET'])
def get_optimal_matrix_image(imageId):
    return send_from_directory('../assets', imageId + '.png')

@router.route('/toggle_left_sprinkler', methods=['POST'])
def toggle_left_sprinkler():
    controller = user_simulations[session['user_id']]['controller']
    controller.toggle_left_sprinkler()
    return Response(status=200)

def start_flask(host, port, ):
    router.run(host=host, port=port)
