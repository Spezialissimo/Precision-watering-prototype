from datetime import datetime

class SensorManager:

    def __init__(self, hardware):
        self.hardware = hardware

    def add_data_collector(self, data_collector):
        self.data_collector = data_collector

    def receiving_thread(self):
        while True:
            values = self.hardware.read_sensor_data()
            values["timestamp"] = datetime.now().timestamp()
            self.data_collector.add_sensor_data(values)