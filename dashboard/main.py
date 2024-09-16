from router.router import start_flask
from threading import Thread
from dotenv import dotenv_values
from controller.controller import Controller

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))

    controller = Controller()

    sensor_thread = Thread(target=controller.receive_sensor_data_thread, args=())
    sensor_thread.start()

    irrigation_thread = Thread(target=controller.compute_irrigation_thread, args=())
    irrigation_thread.start()

    update_dbs_thread = Thread(target=controller.upload_data_thread, args=())
    update_dbs_thread.start()

    start_flask(host,port,controller)
    # flask_thread = Thread(target=start_flask, args=(host, port, controller))
    # flask_thread.start()



