import sqlite3

class Sensor_repository:

    def __init__(self):
        self.con = sqlite3.connect("precision_watering.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS sensors (timestamp INTEGER, x INTEGER, y INTEGER, value FLOAT)")

    def insert_sensor_values(self, batch):
        data_to_insert = []
        for data in batch:
            for sensor in data["data"]:
                data_to_insert.append((data["timestamp"], sensor["x"], sensor["y"], sensor["v"]))
        try:
            self.con.executemany("INSERT INTO sensors VALUES (?, ?, ?, ?)", data_to_insert)
            self.con.commit()
        except sqlite3.Error as e:
            pass
