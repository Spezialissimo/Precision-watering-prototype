import serial
import json
import os
from dotenv import load_dotenv
from time import sleep
from enum import Enum
import random
import threading
import random
import time

load_dotenv()

class PumpState(Enum):
    Off = "off"
    On = "on"

class Hardware:

    def __init__(self) -> None:
        self.pump_state = PumpState.Off
        self.__pumpOpeningThreshold = float(os.getenv("PUMP_OPENING_THRESHOLD", 10))
        self.__maxIrrigationValue = int(os.getenv("IRRIGATION_CHECK_PERIOD", 10))
        self.irrigation_thread = None
        self.sensor_values = {}
        self.sensor_values["10_5"] = 0
        self.sensor_values["10_15"] = 0
        self.sensor_values["10_25"] = 0
        self.sensor_values["30_5"] = 0
        self.sensor_values["30_15"] = 0
        self.sensor_values["30_25"] = 0
        self.left_sprinkler_open = True
        self.initial_pump_time = time.time()

    def irrigate(self, seconds):
        if(self.irrigation_thread != None):
            while self.irrigation_thread.is_alive() == True:
                sleep(0.5)

        self.irrigation_thread = threading.Thread(target=self.__open_pump_for, args=(seconds,)).start()

    def __open_pump_for(self, seconds):
        if seconds >  self.__pumpOpeningThreshold:
            self.open_pump()
            sleep(seconds)
        if seconds < self.__maxIrrigationValue - self.__pumpOpeningThreshold:
            self.close_pump()

    def open_pump(self):
        self.initial_pump_time = time.time()
        self.pump_state = PumpState.On

    def close_pump(self):
        self.initial_pump_time = time.time()
        self.pump_state = PumpState.Off

    def get_pump_state(self):
        return self.pump_state

    def toggle_left_sprinkler(self):
        self.left_sprinkler_open = not self.left_sprinkler_open

    def __update_sensor_values(self):
        def fluctuate(min_val, max_val, current_value, magnitude):
            """Fluttua il valore attuale tra il minimo e il massimo, con un'oscillazione controllata."""
            delta = (random.random() - 0.5) * magnitude  # Oscillazione casuale
            return max(min_val, min(max_val, current_value + delta))

        if self.pump_state == PumpState.Off:

            elapsed_time = time.time() - self.initial_pump_time

            # Imposta la durata della fase di diminuzione rapida (ad esempio 10 secondi)
            rapid_decrease_duration = 3.5

            # Diminuzione rapida all'inizio
            if elapsed_time < rapid_decrease_duration:
                decrease_factor = 4  # Diminuzione più rapida iniziale
                self.sensor_values["10_5"] = max(1, min(99, self.sensor_values["10_5"] - (random.random() * decrease_factor)))
                self.sensor_values["10_15"] = max(1, min(99, self.sensor_values["10_15"] - (random.random() * decrease_factor)))
                self.sensor_values["10_25"] = max(1, min(99, self.sensor_values["10_25"] - (random.random() * decrease_factor)))

                if self.left_sprinkler_open:
                    self.sensor_values["30_5"] = max(1, min(99, self.sensor_values["30_5"] - (random.random() * decrease_factor)))
                    self.sensor_values["30_15"] = max(1, min(99, self.sensor_values["30_15"] - (random.random() * decrease_factor)))
                    self.sensor_values["30_25"] = max(1, min(99, self.sensor_values["30_25"] - (random.random() * decrease_factor)))
            else:
                # Dopo i 10 secondi, diminuire lentamente
                slow_decrease_factor = 2  # Diminuzione più lenta per i valori
                self.sensor_values["10_5"] = max(1, min(99, self.sensor_values["10_5"] - (random.random() * slow_decrease_factor)))
                self.sensor_values["10_15"] = max(1, min(99, self.sensor_values["10_15"] - (random.random() * slow_decrease_factor)))
                self.sensor_values["10_25"] = max(1, min(99, self.sensor_values["10_25"] - (random.random() * slow_decrease_factor)))

                if self.left_sprinkler_open:
                    self.sensor_values["30_5"] = max(1, min(99, self.sensor_values["30_5"] - (random.random() * slow_decrease_factor)))
                    self.sensor_values["30_15"] = max(1, min(99, self.sensor_values["30_15"] - (random.random() * slow_decrease_factor)))
                    self.sensor_values["30_25"] = max(1, min(99, self.sensor_values["30_25"] - (random.random() * slow_decrease_factor)))
                else:
                    # Se il left_sprinkler è chiuso, fluttuano verso il basso tra 1 e 5
                    self.sensor_values["30_5"] = fluctuate(1, 5, self.sensor_values["30_5"], 1)
                    self.sensor_values["30_15"] = fluctuate(1, 5, self.sensor_values["30_15"], 1)
                    self.sensor_values["30_25"] = fluctuate(1, 5, self.sensor_values["30_25"], 1)

        else:
            elapsed_time = time.time() - self.initial_pump_time

            # Imposta la durata della fase di aumento rapido (ad esempio 10 secondi)
            rapid_increase_duration = 4

            # Incremento massimo consentito durante il periodo rapido
            if elapsed_time < rapid_increase_duration:
                increment_factor = 4  # Incremento più rapido iniziale
                # Aumento dei valori, evitando di superare 94
                self.sensor_values["10_5"] = max(1, min(94, self.sensor_values["10_5"] + (random.random() * increment_factor)))
                self.sensor_values["10_15"] = max(1, min(94, self.sensor_values["10_15"] + (random.random() * increment_factor)))
                self.sensor_values["10_25"] = max(1, min(94, self.sensor_values["10_25"] + (random.random() * increment_factor)))

                if self.left_sprinkler_open:
                    self.sensor_values["30_5"] = max(1, min(94, self.sensor_values["30_5"] + (random.random() * increment_factor)))
                    self.sensor_values["30_15"] = max(1, min(94, self.sensor_values["30_15"] + (random.random() * increment_factor)))
                    self.sensor_values["30_25"] = max(1, min(94, self.sensor_values["30_25"] + (random.random() * increment_factor)))
            else:
                # Dopo i 10 secondi, aumentare lentamente verso 95
                # Definiamo un passo di aumento più lento
                slow_increment_factor = 2  # Incremento più lento per i valori
                self.sensor_values["10_5"] = max(1, min(99, self.sensor_values["10_5"] + (random.random() * slow_increment_factor)))
                self.sensor_values["10_15"] = max(1, min(99, self.sensor_values["10_15"] + (random.random() * slow_increment_factor)))
                self.sensor_values["10_25"] = max(1, min(99, self.sensor_values["10_25"] + (random.random() * slow_increment_factor)))

                if self.left_sprinkler_open:
                    self.sensor_values["30_5"] = max(1, min(99, self.sensor_values["30_5"] + (random.random() * slow_increment_factor)))
                    self.sensor_values["30_15"] = max(1, min(99, self.sensor_values["30_15"] + (random.random() * slow_increment_factor)))
                    self.sensor_values["30_25"] = max(1, min(99, self.sensor_values["30_25"] + (random.random() * slow_increment_factor)))
                else:
                    self.sensor_values["30_5"] = fluctuate(1, 5, self.sensor_values["30_5"], 1)
                    self.sensor_values["30_15"] = fluctuate(1, 5, self.sensor_values["30_15"], 1)
                    self.sensor_values["30_25"] = fluctuate(1, 5, self.sensor_values["30_25"], 1)







    def read_sensor_data(self):
        while True:
            self.__update_sensor_values()
            sleep(1)

            return {
                'data': [
                    {
                        'x': 10,
                        'y': 5,
                        'v': self.sensor_values["10_5"]
                    },
                    {
                        'x': 10,
                        'y': 15,
                        'v': self.sensor_values["10_15"]
                    },
                    {
                        'x': 10,
                        'y': 25,
                        'v': self.sensor_values["10_25"]
                    },
                    {
                        'x': 30,
                        'y': 5,
                        'v': self.sensor_values["30_5"]
                    },
                    {
                        'x': 30,
                        'y': 15,
                        'v': self.sensor_values["30_15"]
                    },
                    {
                        'x': 30,
                        'y': 25,
                        'v': self.sensor_values["30_25"]
                    }
                ]
            }
