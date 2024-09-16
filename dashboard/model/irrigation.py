import serial
import json
import os
import csv
from dotenv import load_dotenv
from time import sleep
from datetime import datetime
from hardware.hardware import PumpState

load_dotenv()

class IrrigationMode:
    Manual = 'manual'
    Slider = 'slider'
    Matrix = 'matrix'

    def __str__(self) -> str:
        return self.name

    def name(self):
        return self.name

class IrrigationManager:

    def __init__(self, hardware):
        self.mode = IrrigationMode.Manual
        self.pump = hardware
        self.optimal_value = None
        self.__maxIrrigationValue = int(os.getenv("IRRIGATION_CHECK_PERIOD", 10))
        self.default_optimals = {}
        self.load_optimals()

    def load_optimals(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        asset_folder = '../assets'
        csv_file_name = 'values.csv'
        csv_file_path = os.path.join(base_dir, asset_folder, csv_file_name)

        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"Il file CSV non è stato trovato: {csv_file_path}")

        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                id = row['id']
                title = row['title']
                description = row['description']
                value = json.loads(row['value'].replace("'", '"'))
                self.default_optimals[id] = {
                    'title': title,
                    'description': description,
                    'value': value
                }


    def toggle_pump(self):
        state = self.pump.get_pump_state()
        self.pump.close_pump() if state == PumpState.On else self.pump.open_pump()

    def get_pump_state(self):
        return self.pump.get_pump_state()

    def set_irrigation_mode(self, mode):
        if (mode == IrrigationMode.Manual):
            self.mode = IrrigationMode.Manual
            self.pump.close_pump()
        elif (mode == IrrigationMode.Slider):
            self.mode = IrrigationMode.Slider
        elif (mode == IrrigationMode.Matrix):
            self.mode = IrrigationMode.Matrix
        else:
            raise Exception("Invalid irrigation mode")

    def set_new_optimal_value(self, value):
        self.optimal_value = value

    def set_new_optimal_matrix(self, matrix):
        self.optimal_matrix = {
                    'title': "",
                    'description': "",
                    'value': matrix
                }

    def __compute_average(self, sensors):
        if not sensors:
            return 0
        total = sum(sensor["v"] for sensor in sensors)
        average = total / len(sensors)
        return average

    def compute_irrigation(self, last_sensor_data, last_irrigation_data):
        current_moisture = self.__compute_average(last_sensor_data['data'])
        old_irrigation = last_irrigation_data["irrigation"]
        old_r = last_irrigation_data["r"]
        mode = self.mode
        if (mode == IrrigationMode.Slider and self.optimal_value != None):
            r = self.optimal_value - current_moisture
            optimal_moisture = self.optimal_value
        elif (mode == IrrigationMode.Matrix and self.optimal_matrix != None):
            diffs = []
            for measurement in last_sensor_data["data"]:
                for o_m in self.optimal_matrix['value']:
                    if o_m['x'] == measurement['x'] and o_m['y'] == measurement['y']:
                        optimal = o_m
                        break
                diffs.append(optimal["v"] - measurement["v"])
            r = sum(diffs) / len(diffs)
            optimal_moisture = self.__compute_average(self.optimal_matrix['value'])
        elif (mode == IrrigationMode.Manual):
            irrigation_data = {
                "timestamp": datetime.now().timestamp(),
                "r": 0,
                "irrigation": 0,
                "optimal_m": 0,
                "current_m": current_moisture
            }

        if mode != IrrigationMode.Manual:
            kp=0.3
            ki=0.5
            new_irrigation = min(max(0, old_irrigation + kp * (r - old_r) + ki * r), self.__maxIrrigationValue)
            irrigation_data = {
                "timestamp": datetime.now().timestamp(),
                "r": r,
                "irrigation": new_irrigation,
                "optimal_m": optimal_moisture,
                "current_m": current_moisture
            }
            self.pump.irrigate(new_irrigation)
        else:
            new_irrigation = 0

        return irrigation_data

    def get_optimals(self):
        return self.default_optimals

    def get_optimal_matrix(self):
        return self.optimal_matrix