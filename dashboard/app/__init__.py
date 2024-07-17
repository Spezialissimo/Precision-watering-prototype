# app/__init__.py
import sys

print(sys.path)

from flask import Flask

app = Flask(__name__)

import app.index  # Ensure routes and functions are loaded
