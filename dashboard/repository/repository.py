import sqlite3

class Repository:

    def __init__(self):
        self.con = sqlite3.connect("sensors.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS sensors (timestamp INTEGER, x INTEGER, y INTEGER, value FLOAT)")

    def insert_sensor_values(self, batch):
        for data in batch:
            for sensor in data["data"]:
                try:
                    self.con.execute("INSERT INTO sensors VALUES (?, ?, ?, ?)", (data["timestamp"], sensor["x"], sensor["y"], sensor["v"]))
                except ex:                    
                    pass
        self.con.commit()
