import serial
import json
import os
from dotenv import load_dotenv
from time import sleep
from enum import Enum
import random
import threading
import random
import time

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
        self.left_sprinkler_open = True
        self.initial_pump_time = time.time()

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
        self.initial_pump_time = time.time()
        self.pump_state = PumpState.On

    def close_pump(self):
        self.initial_pump_time = time.time()
        self.pump_state = PumpState.Off

    def get_pump_state(self):
        return self.pump_state

    def toggle_left_sprinkler(self):
        self.left_sprinkler_open = not self.left_sprinkler_open

    def __update_sensor_values(self):
        self.__FLACTUATE_MIN_INCREASE = 90
        self.__FLACTUATE_MAX_INCREASE = 99
        self.__FLACTUATE_MIN_DECREASE = 1
        self.__FLACTUATE_MAX_DECREASE = 10
        self.__THRESHOLD_RAPID_INCREASE = 4
        self.__THRESHOLD_RAPID_DECREASE = 3.5
        self.__DECREASE_FACTOR_RAPID = 6
        self.__DECREASE_FACTOR_SLOW = 2
        self.__INCREASE_FACTOR_RAPID = 8
        self.__INCREASE_FACTOR_SLOW = 3

        def new_value_pump_off(current_value, decrease_factor):
            if current_value < self.__FLACTUATE_MAX_DECREASE:
                return fluctuate(self.__FLACTUATE_MIN_DECREASE, self.__FLACTUATE_MAX_DECREASE, current_value, 3)
            else:
                return max(self.__FLACTUATE_MIN_DECREASE, min(99, current_value - (random.random() * decrease_factor)))
        def new_value_pump_on(current_value, decrease_factor):
            if current_value > self.__FLACTUATE_MIN_INCREASE:
                return fluctuate(self.__FLACTUATE_MIN_INCREASE, self.__FLACTUATE_MAX_INCREASE, current_value, 3)
            else:
                return max(1, min(self.__FLACTUATE_MAX_INCREASE, current_value + (random.random() * decrease_factor)))

        def fluctuate(min_val, max_val, current_value, magnitude):
            """Fluttua il valore attuale tra il minimo e il massimo, con un'oscillazione controllata."""
            delta = (random.random() - 0.5) * magnitude  # Oscillazione casuale
            return max(min_val, min(max_val, current_value + delta))

        if self.pump_state == PumpState.Off:

            elapsed_time = time.time() - self.initial_pump_time

            rapid_decrease_duration = self.__THRESHOLD_RAPID_DECREASE

            if elapsed_time < rapid_decrease_duration:
                decrease_factor = self.__DECREASE_FACTOR_RAPID
            else:
                decrease_factor = self.__DECREASE_FACTOR_SLOW

            for sensor in self.sensor_values:
                self.sensor_values[sensor] = new_value_pump_off(self.sensor_values[sensor], decrease_factor)

        else:
            elapsed_time = time.time() - self.initial_pump_time

            rapid_increase_duration = self.__THRESHOLD_RAPID_INCREASE

            if elapsed_time < rapid_increase_duration:
                increment_factor = self.__INCREASE_FACTOR_RAPID
            else:
                increment_factor = self.__INCREASE_FACTOR_SLOW

            for sensor in self.sensor_values:
                if self.left_sprinkler_open:
                    self.sensor_values[sensor] = new_value_pump_on(self.sensor_values[sensor], increment_factor)
                else:
                    if(sensor == "30_5" or sensor == "30_15" or sensor == "30_25"):
                        self.sensor_values[sensor] = new_value_pump_off(self.sensor_values[sensor], self.__DECREASE_FACTOR_RAPID)
                    else:
                        self.sensor_values[sensor] = new_value_pump_on(self.sensor_values[sensor], increment_factor)





    def read_sensor_data(self):
        while True:
            self.__update_sensor_values()
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
