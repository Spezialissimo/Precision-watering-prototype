import serial
import json
import os
from dotenv import load_dotenv
from time import sleep
from enum import Enum
import random
import threading

load_dotenv()

class PumpState(Enum):
    Off = "off"
    On = "on"

class Hardware:

    def __init__(self) -> None:
        self.pump_state = PumpState.Off
        self.__pumpOpeningThreshold = float(os.getenv("PUMP_OPENING_THRESHOLD", 10))
        self.__maxIrrigationValue = int(os.getenv("IRRIGATION_CHECK_PERIOD", 10))
        self.irrigation_thread = None
        self.sensor_values = {}
        self.sensor_values["10_5"] = 0
        self.sensor_values["10_15"] = 0
        self.sensor_values["10_25"] = 0
        self.sensor_values["30_5"] = 0
        self.sensor_values["30_15"] = 0
        self.sensor_values["30_25"] = 0

    def irrigate(self, seconds):
        if(self.irrigation_thread != None):
            while self.irrigation_thread.is_alive() == True:
                sleep(0.5)

        self.irrigation_thread = threading.Thread(target=self.__open_pump_for, args=(seconds,)).start()

    def __open_pump_for(self, seconds):
        if seconds >  self.__pumpOpeningThreshold:
            self.open_pump()
            sleep(seconds)
        if seconds < self.__maxIrrigationValue - self.__pumpOpeningThreshold:
            self.close_pump()

    def open_pump(self):
        self.pump_state = PumpState.On

    def close_pump(self):
        self.pump_state = PumpState.Off

    def get_pump_state(self):
        return self.pump_state

    def read_sensor_data(self):
        while True:
            if self.pump_state == PumpState.Off:
                self.sensor_values["10_5"] = max(0, min (100,self.sensor_values["10_5"] - (random.random() % 3)))
                self.sensor_values["10_15"] = max(0, min (100,self.sensor_values["10_15"] - (random.random() % 3)))
                self.sensor_values["10_25"] = max(0, min (100,self.sensor_values["10_25"] - (random.random() % 3)))
                self.sensor_values["30_5"] = max(0, min (100,self.sensor_values["30_5"] - (random.random() % 3)))
                self.sensor_values["30_15"] = max(0, min (100,self.sensor_values["30_15"] - (random.random() % 3)))
                self.sensor_values["30_25"] = max(0, min (100,self.sensor_values["30_25"] - (random.random() % 3)))
            else:
                self.sensor_values["10_5"] = max(0, min (100, self.sensor_values["10_5"] + (random.random() % 3)))
                self.sensor_values["10_15"] = max(0, min (100, self.sensor_values["10_15"] + (random.random() % 3)))
                self.sensor_values["10_25"] = max(0, min (100, self.sensor_values["10_25"] + (random.random() % 3)))
                self.sensor_values["30_5"] = max(0, min (100, self.sensor_values["30_5"]  + (random.random() % 3)))
                self.sensor_values["30_15"] = max(0, min (100, self.sensor_values["30_15"] + (random.random() % 3)))
                self.sensor_values["30_25"] = max(0, min (100, self.sensor_values["30_25"] + (random.random() % 3)))

            sleep(1)

            return {
                'data': [
                    {
                        'x': 10,
                        'y': 5,
                        'v': self.sensor_values["10_5"]
                    },
                    {
                        'x': 10,
                        'y': 15,
                        'v': self.sensor_values["10_15"]
                    },
                    {
                        'x': 10,
                        'y': 25,
                        'v': self.sensor_values["10_25"]
                    },
                    {
                        'x': 30,
                        'y': 5,
                        'v': self.sensor_values["30_5"]
                    },
                    {
                        'x': 30,
                        'y': 15,
                        'v': self.sensor_values["30_15"]
                    },
                    {
                        'x': 30,
                        'y': 25,
                        'v': self.sensor_values["30_25"]
                    }
                ]
            }
