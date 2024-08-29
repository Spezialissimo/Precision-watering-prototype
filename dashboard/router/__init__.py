# app/__init__.py
import sys


from flask import Flask
from flask_socketio import SocketIO




import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

router = Flask(__name__)
socketio = SocketIO(router)

import router.router
import socketio