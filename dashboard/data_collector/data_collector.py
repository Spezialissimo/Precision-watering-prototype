from repository.data import get_all_irrigation_data, save_irrigation_data, should_restore_backup
from interpolator.interpolator import interpolate_data
import time

class DataCollector:

    def __init__(self, sensor_manager, irrigation_manager, hardware):
        self.sensor_data = []
        self.sensor_data_with_interpolation = []
        self.irrigation_data = []
        self.hardware = hardware
        self.sensor_manager = sensor_manager
        self.irrigation_manager = irrigation_manager
        self.sensor_manager.add_data_collector(self)
        self.irrigation_manager.add_data_collector(self)
        if should_restore_backup():
            self.irrigation_data = get_all_irrigation_data()


    def get_all_sensor_data(self, seconds=None):
        if seconds is not None:
            end_time = time.time()
            start_time = end_time - seconds
            result = [row for row in self.sensor_data if start_time <= float(row["timestamp"]) <= end_time]
        else:
            result = self.sensor_data
        return result

    def get_all_sensor_data_with_interpolation(self, seconds=None):
        if seconds is not None:
            end_time = time.time()
            start_time = end_time - seconds
            result = [row for row in self.sensor_data_with_interpolation if start_time <= float(row["timestamp"]) <= end_time]
        else:
            result = self.sensor_data_with_interpolation
        return result

    def get_last_sensor_data(self):
        return self.sensor_data[-1] if self.sensor_data else None

    def get_last_sensor_data_with_interpolation(self):
        return self.sensor_data_with_interpolation[-1] if self.sensor_data_with_interpolation else None

    def get_all_irrigation_data(self, seconds=None):
        if len(self.irrigation_data) == 0:
            return []

        if seconds is not None:
            end_time = time.time()
            start_time = end_time - seconds
            result = [row for row in self.irrigation_data if start_time <= float(row["timestamp"]) <= end_time]
        else:
            result = self.irrigation_data
        return result

    def get_last_irrigation_data(self):
        return self.irrigation_data[-1] if self.irrigation_data else None

    def get_pump_state(self):
        return self.irrigation_manager.get_pump_state()

    def set_irrigation_mode(self, mode):
        self.irrigation_manager.set_irrigation_mode(mode)

    def set_new_optimal_value(self, value):
        self.irrigation_manager.set_new_optimal_value(value)

    def set_new_optimal_matrix(self, matrix):
        self.irrigation_manager.set_new_optimal_matrix(matrix)

    def toggle_pump(self):
        self.irrigation_manager.toggle_pump()

    def get_last_sensor_data_average(self):
        sensors = self.get_last_sensor_data()
        if not sensors:
            return None
        total = sum(sensor["v"] for sensor in sensors['data'])
        average = total / len(sensors['data'])
        return average

    def add_sensor_data(self, data):
        self.sensor_data.append(data)
        interpolated_data = interpolate_data(data["data"], [10, 30], [5, 15, 25])
        self.sensor_data_with_interpolation.append({"timestamp": data["timestamp"], "data": interpolated_data})

    def add_irrigation_data(self, data):
        save_irrigation_data(data)
        self.irrigation_data.append(data)

    def get_optimals(self):
        return self.irrigation_manager.get_optimals()

