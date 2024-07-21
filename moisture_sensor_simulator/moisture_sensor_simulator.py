import tkinter as tk
from tkinter import ttk
import json
import serial
import threading

## Prima di eseguire il simulatore, assicurarsi di avere configurato la porta seriale in modo che sia accessibile dal simulatore
## In linux: socat -d -d PTY,link=/tmp/ttyV0,raw,echo=0 PTY,link=/tmp/ttyV1,raw,echo=0
## Ovviamente è necessario cambiare in .env di dashboard il valore di SERIAL_PORT.

SERIAL_PORT = '/tmp/ttyV0'  # Porta seriale virtuale di invio
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

class HardwareSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hardware Simulator")

        self.sliders = []
        self.slider_values = [
            {"x": 10, "y": 5, "v": 0},
            {"x": 10, "y": 15, "v": 0},
            {"x": 10, "y": 25, "v": 0},
            {"x": 30, "y": 5, "v": 0},
            {"x": 30, "y": 15, "v": 0},
            {"x": 30, "y": 25, "v": 0}
        ]

        for i in range(6):
            slider = ttk.Scale(self.root, from_=0, to=100, orient='horizontal', command=lambda v, idx=i: self.update_value(v, idx))
            slider.grid(row=i%3, column=i % 2, padx=10, pady=5)
            self.sliders.append(slider)

        self.led_status = False
        self.led_label = tk.Label(self.root, text="LED", width=10, height=2, bg="red")
        self.led_label.grid(row=4, column=0, rowspan=6, padx=10, pady=5)

        self.serial_thread = threading.Thread(target=self.read_serial)
        self.serial_thread.daemon = True
        self.serial_thread.start()

        self.update_data()

    def update_value(self, value, idx):
        self.slider_values[idx]["v"] = int(float(value))

    def update_data(self):
        data = json.dumps({"data": self.slider_values})
        ser.write(data.encode()+b'\n')
        self.root.after(100, self.update_data)

    def read_serial(self):
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                if data == '1':
                    self.update_led_status(True)
                elif data == '0':
                    self.update_led_status(False)

    def update_led_status(self, status):
        self.led_status = status
        self.led_label.config(bg="green" if status else "red")

def main():
    root = tk.Tk()
    app = HardwareSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
