# app/__init__.py
import sys

from flask import Flask

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

router = Flask(__name__)

import router.router