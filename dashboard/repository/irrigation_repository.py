import sqlite3

class Irrigation_repository:

    def __init__(self):
        self.con = sqlite3.connect("precision_watering.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS irrigation (timestamp INTEGER, r INTEGER, irrigation INTEGER, optimal_m FLOAT, current_m FLOAT)")

    def insert_irrigation_values(self, batch):
        for irrigation_data in batch:
            try:
                self.con.execute("INSERT INTO irrigation VALUES (?, ?, ?, ?, ?)", (irrigation_data["timestamp"], irrigation_data["r"], irrigation_data["irrigation"], irrigation_data["optimal_m"], irrigation_data["current_m"]))
            except:                    
                pass
        self.con.commit()
