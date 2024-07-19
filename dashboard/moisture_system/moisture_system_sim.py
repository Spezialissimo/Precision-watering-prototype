import serial
from datetime import datetime
import pytz
import json
import numpy as np
from scipy.interpolate import interpn
import threading
from repository.data import save_sensor_data
from dotenv import dotenv_values

tz = pytz.timezone("Europe/Rome")
pump_state = False
lock = threading.Lock()

def togglePump():
    pass

def receive():
    pass
