import requests
import time
import os
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

from remote_manager.remote_manager import RemoteManager
from repository.sensor_repository import SensorRepository
from repository.irrigation_repository import IrrigationRepository
from model.irrigation import IrrigationManager
from model.sensors import SensorManager
from hardware.hardware import Hardware
from interpolator.interpolator import interpolate_data

class Controller:

    def __init__(self):
        self.__last_sensor_data = None
        self.__last_irrigation_data = [self.__get_empty_irrigation_data()]
        self.__stop_uploading = True
        hardware = Hardware()
        self.__irrigation_manager = IrrigationManager(hardware)
        self.__sensor_manager = SensorManager(hardware)
        self.__irrigationCheckPeriod = int(os.getenv("IRRIGATION_CHECK_PERIOD", 10))


    def get_last_sensor_data(self):
        if self.__last_sensor_data == None:
            sleep(1)
        return self.__last_sensor_data

    def get_last_sensor_data_with_interpolation(self):
        sensor_data = self.get_last_sensor_data()
        return {
                    'data': interpolate_data(sensor_data['data'], [10, 30], [5, 15, 25]),
                    'timestamp': sensor_data['timestamp']
                }

    def get_last_irrigation_data(self):
        return self.__last_irrigation_data[-1] if self.__last_irrigation_data else self.__get_empty_irrigation_data()

    def __get_empty_irrigation_data(self):
        return {"timestamp": datetime.now().timestamp(), "r": 0, "irrigation": 0, "optimal_m": 0, "current_m": 0}

    def get_pump_state(self):
        return self.__irrigation_manager.get_pump_state()

    def set_irrigation_mode(self, mode):
        self.__irrigation_manager.set_irrigation_mode(mode)

    def set_new_optimal_value(self, value):
        self.__irrigation_manager.set_new_optimal_value(value)

    def set_new_optimal_matrix(self, matrix):
        self.__irrigation_manager.set_new_optimal_matrix(matrix)

    def toggle_pump(self):
        self.__irrigation_manager.toggle_pump()

    def get_optimal_matrix_average(self):
        optimal = self.__irrigation_manager.get_optimal_matrix()
        if not optimal:
            return None
        total = sum(sensor["v"] for sensor in optimal['value'])
        average = total / len(optimal['value'])
        return average

    def compute_irrigation_thread(self):
        while True:
            last_sensor_data = self.get_last_sensor_data()
            last_irrigation_data = self.get_last_irrigation_data()
            if(last_sensor_data == None):
                sleep(1)
                continue
            irrigation = self.__irrigation_manager.compute_irrigation(last_sensor_data=last_sensor_data, last_irrigation_data=last_irrigation_data)
            self.__last_irrigation_data.append(irrigation)
            sleep(self.__irrigationCheckPeriod)

    def receive_sensor_data_thread(self):
        while True:
            sensor_data = self.__sensor_manager.receive_sensor_data()
            self.__last_sensor_data = sensor_data

    def get_optimals(self):
        return self.__irrigation_manager.get_optimals()

    def toggle_left_sprinkler(self):
        self.__sensor_manager.toggle_left_sprinkler()