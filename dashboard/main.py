from router.router import start_flask
from threading import Thread
from dotenv import dotenv_values
from sensor_manager.sensor_manager import SensorManager
from irrigation_manager.irrigation_manager import IrrigationManager
from hardware.hardware import Hardware
from data_collector.data_collector import DataCollector

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))

    hw = Hardware()
    sm = SensorManager(hw)
    im = IrrigationManager(hw)
    dc = DataCollector(sensor_manager=sm, irrigation_manager=im, hardware=hw)

    sensor_thread = Thread(target=sm.receiving_thread, args=())
    sensor_thread.start()

    irrigation_thread = Thread(target=im.compute_irrigation_thread, args=())
    irrigation_thread.start()

    flask_thread = Thread(target=start_flask, args=(host, port, dc))
    flask_thread.start()



