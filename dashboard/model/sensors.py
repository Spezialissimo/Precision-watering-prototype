from datetime import datetime

class SensorManager:

    def __init__(self, hardware):
        self.hardware = hardware

    def receive_sensor_data(self):
            values = self.hardware.read_sensor_data()
            values["timestamp"] = datetime.now().timestamp()
            return values

    def toggle_left_sprinkler(self):
        self.hardware.toggle_left_sprinkler()