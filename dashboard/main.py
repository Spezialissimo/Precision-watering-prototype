from app.index import start_flask
from moisture_system.moisture_system import receive
from threading import Thread
from dotenv import dotenv_values, load_dotenv

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))
    serial_port = config.get("SERIAL_PORT", "/dev/ttyACM0")
    baudrate = int(config.get("SERIAL_BAUDRATE", 9600))

    receiving_thread = Thread(target=receive, args=(serial_port, baudrate))
    receiving_thread.start()

    # start_flask(host, port)
    flask_thread = Thread(target=start_flask, args=(host, port))
    flask_thread.start()

