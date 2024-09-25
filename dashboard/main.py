from router.router import start_flask
from threading import Thread
from dotenv import dotenv_values
from controller.controller import Controller

if __name__ == '__main__':
    config = dotenv_values(".env")
    host = config.get("HOST", "0.0.0.0")
    port = int(config.get("PORT", 5000))

    start_flask(host,port)



