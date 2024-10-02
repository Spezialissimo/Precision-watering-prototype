import sqlite3

class IrrigationRepository:

    def __init__(self):
        self.con = sqlite3.connect("precision_watering.db")
        self.con.execute("CREATE TABLE IF NOT EXISTS irrigation (timestamp INTEGER, r INTEGER, irrigation INTEGER, optimal_m FLOAT, current_m FLOAT)")

    def insert_irrigation_values(self, batch):
        data_to_insert = []
        for irrigation_data in batch:
            data_to_insert.append((
                irrigation_data["timestamp"],
                irrigation_data["r"],
                irrigation_data["irrigation"],
                irrigation_data["optimal_m"],
                irrigation_data["current_m"]
            ))
        try:
            self.con.executemany("INSERT INTO irrigation VALUES (?, ?, ?, ?, ?)", data_to_insert)
            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
