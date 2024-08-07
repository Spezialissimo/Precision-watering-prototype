from dotenv import dotenv_values
from time import sleep
from datetime import datetime
from hardware.hardware import PumpState
import os
import json
import csv

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
        self.__maxIrrigationValue = int(dotenv_values(".env")["IRRIGATION_CHECK_PERIOD"])
        self.__irrigationCheckPeriod = int(dotenv_values(".env")["IRRIGATION_CHECK_PERIOD"])
        self.optimals = {}
        self.load_optimals()

    def load_optimals(self):
        asset_folder = 'assets'
        csv_file_path = os.path.join(asset_folder, 'values.csv')
        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                id = row['id']
                title = row['title']
                description = row['description']
                value = json.loads(row['value'].replace("'", '"'))
                self.optimals[id] = {
                    'title': title,
                    'description': description,
                    'value': value
                }

    def add_data_collector(self, data_collector):
        self.data_collector = data_collector

    def __open_pump_for(self,seconds):
        if seconds > 0 :
            self.pump.open_pump()
            sleep(seconds)
        if seconds < self.__maxIrrigationValue:
            self.pump.close_pump()


    def toggle_pump(self):
        if (self.mode != IrrigationMode.Manual):
            raise Exception("Pump can be toggled only in manual mode")
        state = self.pump.get_pump_state()
        self.pump.close_pump() if state == PumpState.On else self.pump.open_pump()

    def get_pump_state(self):
        return self.pump.get_pump_state()

    def set_irrigation_mode(self, mode):
        if (mode == IrrigationMode.Manual):
            self.mode = IrrigationMode.Manual
        elif (mode == IrrigationMode.Slider):
            self.mode = IrrigationMode.Slider
        elif (mode == IrrigationMode.Matrix):
            self.mode = IrrigationMode.Matrix
        else:
            raise Exception("Invalid irrigation mode")

    def set_new_optimal_value(self, value):
        if (self.mode != IrrigationMode.Slider):
            raise Exception("Optimal value can be set only in slider mode")
        self.optimal_value = value

    def set_new_optimal_matrix(self, matrix):
        if (self.mode != IrrigationMode.Matrix):
            raise Exception("Optimal matrix can be set only in matrix mode")
        self.optimal_matrix = self.optimals[matrix]

    def compute_irrigation_thread(self):
        while True:
            current_moisture = self.data_collector.get_last_sensor_data_average()
            if (self.mode == IrrigationMode.Slider and self.optimal_value != None):
                lastIrrigationData = self.data_collector.get_last_irrigation_data()
                if(lastIrrigationData == None or lastIrrigationData["irrigation"] == "" or lastIrrigationData["r"] == ""):
                    oldIrrigation = 0
                    oldR = 0
                else:
                    oldIrrigation = lastIrrigationData["irrigation"]
                    oldR = lastIrrigationData["r"]

                r = self.optimal_value - current_moisture
                optimal_moisture = self.optimal_value
            elif (self.mode == IrrigationMode.Matrix and self.optimal_matrix != None):
                lastIrrigationData = self.data_collector.get_last_irrigation_data()
                if(lastIrrigationData == None or lastIrrigationData["irrigation"] == "" or lastIrrigationData["r"] == ""):
                    oldIrrigation = 0
                    oldR = 0
                else:
                    oldIrrigation = lastIrrigationData["irrigation"]
                    oldR = lastIrrigationData["r"]

                lastSensorData = self.data_collector.get_last_sensor_data()
                diffs = []
                for measurement in lastSensorData["data"]:
                    for o_m in self.optimal_matrix['value']['data']:
                        if o_m['x'] == measurement['x'] and o_m['y'] == measurement['y']:
                            optimal = o_m
                            break
                    diffs.append(optimal["v"] - measurement["v"])

                r = sum(diffs) / len(diffs)
                optimal_moisture = self.data_collector.get_optimal_matrix_average()

            elif (self.mode == IrrigationMode.Manual):
                irrigation_data = {
                    "timestamp": datetime.now().timestamp(),
                    "r": 0,
                    "irrigation": 0,
                    "optimal_m": 0,
                    "current_m": current_moisture if current_moisture is not None else 0.0
                }

            if self.mode != IrrigationMode.Manual:
                kp=0.3
                ki=0.5
                new_irrigation = min(max(0, oldIrrigation + kp * (r - oldR) + ki * r), self.__maxIrrigationValue)
                irrigation_data = {
                    "timestamp": datetime.now().timestamp(),
                    "r": r,
                    "irrigation": new_irrigation,
                    "optimal_m": optimal_moisture,
                    "current_m": current_moisture
                }
                print(f"Irrigation data added: {irrigation_data}")
                self.__open_pump_for(new_irrigation)
            else:
                print(f"Irrigation data added: {irrigation_data}")
                new_irrigation = 0

            self.data_collector.add_irrigation_data(irrigation_data)
            sleep(self.__irrigationCheckPeriod - new_irrigation)

    def  get_optimals(self):
        return self.optimals

    def get_optimal_matrix(self):
        return self.optimal_matrix