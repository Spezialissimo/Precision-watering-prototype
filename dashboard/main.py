from app.index import start_flask
from moisture_system.moisture_system import receive, compute_irrigation
from threading import Thread
from dotenv import dotenv_values, load_dotenv

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))

    receiving_thread = Thread(target=receive, args=())
    receiving_thread.start()

    receiving_thread = Thread(target=compute_irrigation, args=())
    receiving_thread.start()

    flask_thread = Thread(target=start_flask, args=(host, port))
    flask_thread.start()

