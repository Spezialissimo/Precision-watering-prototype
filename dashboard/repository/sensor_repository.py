import sqlite3

class Sensor_repository:

    def __init__(self):
        self.con = sqlite3.connect("precision_watering.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS sensors (timestamp INTEGER, x INTEGER, y INTEGER, value FLOAT)")

    def insert_sensor_values(self, batch):
        for data in batch:
            for sensor in data["data"]:
                try:
                    self.con.execute("INSERT INTO sensors VALUES (?, ?, ?, ?)", (data["timestamp"], sensor["x"], sensor["y"], sensor["v"]))
                except:                    
                    pass
        self.con.commit()
