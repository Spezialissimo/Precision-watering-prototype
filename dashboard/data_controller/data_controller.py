import requests
from repository.sensor_repository import Sensor_repository
from repository.irrigation_repository import Irrigation_repository
from time import sleep
import os

from datetime import datetime
fiware_api_datetime_format = "%Y-%m-%dT%H:%M:%S"

class DataController:

    def update_dbs(self):
        self.sensor_repository = Sensor_repository()
        self.irrigation_repository = Irrigation_repository()
        while True:
            sleep(60)
            last_sensor_data = self.data_collector.get_all_sensor_data()[1:]
            if(last_sensor_data != None and len(last_sensor_data) > 0):
                data = self.aggregate_sensor_data(last_sensor_data)
                self.send_sensor_data_to_db(data)
                self.send_sensor_data_to_FIWARE(data)

            to_skip = int(os.getenv("NUMBER_OF_IRRIGATION_DATA_TO_KEEP_IN_MEMORY", 10))
            last_irrigation_data = self.data_collector.get_all_irrigation_data()[to_skip:]
            if(last_irrigation_data != None and len(last_irrigation_data) > 0):
                self.send_irrigation_data_to_db(last_irrigation_data)
                self.send_irrigation_data_to_FIWARE(last_irrigation_data)

    def __init__(self, data_collector):
        self.data_collector = data_collector

    def aggregate_sensor_data(self, data):
        new_data = []
        for i in range(len(data)):
            if i % 2 == 0:
                new_data.append(data[i])
        return new_data

    def send_sensor_data_to_db(self, data):
        self.sensor_repository.insert_sensor_values(data)

    def send_irrigation_data_to_db(self, data):
        self.irrigation_repository.insert_irrigation_values(data)


    def send_sensor_data_to_FIWARE(self, batch):
        for data in batch:
            for sensor in data["data"]:
                sensor_pos = str(sensor["x"]) + "_" + str(sensor["y"])
                sensor_value = sensor["v"]
                measurement_date = datetime.fromtimestamp(data["timestamp"]).strftime(fiware_api_datetime_format)
                output_data = self.build_fiware_sensor_update(sensor_pos, sensor_value, measurement_date)
                print(output_data)

    def send_irrigation_data_to_FIWARE(self, batch):
        for irrigation_data in batch:
            irrigation_data["timestamp"] = datetime.fromtimestamp(irrigation_data["timestamp"]).strftime(fiware_api_datetime_format)
            output_data = self.build_fiware_irrigation_update(irrigation_data)
            print(output_data)

    def send_to_FIWARE(self, data):
        try:
            params = {"options": "keyValues"}
            update_body = {"actionType": "append", "entities": [data]}

            response = requests.post(
                endpoint_url_update_entity, params=params, json=update_body
            )
            response.raise_for_status()
            if response.status_code >= 200 and response.status_code < 300:
                print("Successfully updated FIWARE entity")
        except Exception as e:
            print(e)
            print(e.__doc__)

    def build_fiware_irrigation_update(self, irrigation_data):
        return {
            "id": "urn:ngsi-ld:Device:unibo:56945b53-06f6-4251-a079-8e6d9564b523",
            "name": "UniBO Dripper NDR",
            "description": "Researcher night simulation dripper",
            "type": "Device",
            "category":[ "sensor" ],
            "function": [ "sensing" ],
            "controlledProperty":[ "waterConsumption" ],
            "supportedUnits": ["LTR"],
            "value": [f"{irrigation_data['irrigation']}"],
            "dateObserved": f"{irrigation_data['timestamp']}",
            "namespace": "unibo.ndr",
            "location":{ "type": "Point", "coordinates": [12.235930, 44.147788] },
        }

    def build_fiware_sensor_update(self, sensor_pos, sensor_value, measurement_date):
        return {
            "id": f"urn:ngsi-ld:Device:unibo:ndr_pinotech__{sensor_pos}",
            "name": f"Pinotech Soil Moisture {sensor_pos}",
            "description": "Researcher night simulation sensor",
            "type": "Device",
            "category": ["sensor"],
            "controlledProperty": ["soilMoisture"],
            "supportedUnits": ["P1"],
            "value": [f"{sensor_value}"],
            "refDeviceModel": "urn:ngsi-ld:DeviceModel:unibo:f757454d-66a4-41c5-8abf-a5848ab41191",
            "dateObserved": f"{measurement_date}",
            "location": {"type": "Point", "coordinates": [44.138811, 12.244149]},
        }

