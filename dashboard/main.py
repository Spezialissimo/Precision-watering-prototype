from router.router import start_flask
from threading import Thread
from dotenv import dotenv_values
from sensor_manager.sensor_manager import SensorManager
from irrigation_manager.irrigation_manager import IrrigationManager
from hardware.hardware import Hardware
from data_collector.data_collector import DataCollector
from data_controller.data_controller import DataController

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))

    hardware = Hardware()
    sensor_manager = SensorManager(hardware)
    irrigation_manager = IrrigationManager(hardware)
    data_collector = DataCollector(sensor_manager=sensor_manager, irrigation_manager=irrigation_manager, hardware=hardware)
    data_conntroller = DataController(data_collector)

    sensor_thread = Thread(target=sensor_manager.receiving_thread, args=())
    sensor_thread.start()

    irrigation_thread = Thread(target=irrigation_manager.compute_irrigation_thread, args=())
    irrigation_thread.start()

    update_dbs_thread = Thread(target=data_conntroller.update_dbs, args=())
    update_dbs_thread.start()

    flask_thread = Thread(target=start_flask, args=(host, port, data_collector, data_conntroller))
    flask_thread.start()



