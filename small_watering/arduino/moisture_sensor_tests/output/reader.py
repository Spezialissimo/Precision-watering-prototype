import serial
import csv
from datetime import datetime
import time
import pytz
import pandas as pd

tz = pytz.timezone("Europe/Rome")

# Impostazioni della porta seriale
SERIAL_PORT = 'COM4'  # Inserisci qui la tua porta seriale (es. COM3 su Windows)
SERIAL_BAUDRATE = 9600


# Apre la connessione seriale
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

first = True
while True:
    # Legge una riga dal monitor seriale
    moisture_values = ser.readline().decode('utf-8').strip()

    print(moisture_values)
    if moisture_values != "" and ',' in moisture_values:
        sx_moisture_value = moisture_values.split(",")[0]
        dx_moisture_value = moisture_values.split(",")[1]

        # Ottiene il timestamp corrente
        timestamp = datetime.now(tz=tz).replace(microsecond=0)#.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        new_row = pd.DataFrame([[timestamp, sx_moisture_value, dx_moisture_value]], columns=["timestamp", "sx_moisture_value", "dx_moisture_value"])

        if first:
            new_row.to_csv("moisture_values.csv", mode='w', index=False)
            first = False
        else:
            new_row.to_csv("moisture_values.csv", mode='a+', header=False, index=False)