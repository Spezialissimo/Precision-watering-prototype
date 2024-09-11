import requests
from repository.sensor_repository import Sensor_repository
from repository.irrigation_repository import Irrigation_repository
from time import sleep
import os
from datetime import datetime
fiware_api_datetime_format = "%Y-%m-%dT%H:%M:%S"
endpoint_url_update_entity = os.getenv("FIWARE_UPDATE_ENTITY_URL")
from dotenv import load_dotenv

load_dotenv()

class DataController:

    def update_dbs(self):
        self.sensor_repository = Sensor_repository()
        self.irrigation_repository = Irrigation_repository()
        while True:
            sleep(60)
            if self.stop_uploading == False:
                last_sensor_data = self.data_collector.get_all_sensor_data()[:2]
                if(last_sensor_data != None and len(last_sensor_data) > 0):
                    data = self.aggregate_sensor_data(last_sensor_data)
                    self.send_sensor_data_to_db(data)
                    self.send_sensor_data_to_FIWARE(data)

                to_skip = int(os.getenv("NUMBER_OF_IRRIGATION_DATA_TO_KEEP_IN_MEMORY", 10))
                last_irrigation_data = self.data_collector.get_all_irrigation_data()[to_skip:]
                if(last_irrigation_data != None and len(last_irrigation_data) > 0):
                    self.send_irrigation_data_to_db(last_irrigation_data)
                    self.send_irrigation_data_to_FIWARE(last_irrigation_data)

    def stop_upload(self):
        self.stop_uploading = True

    def start_upload(self):
        self.stop_uploading = False

    def is_upload_on(self):
        return self.stop_uploading == False

    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.stop_uploading = True
        if endpoint_url_update_entity is None:
            raise ValueError("Environment variable 'ENDPOINT_URL_UPDATE_ENTITY' is not set")

    def aggregate_sensor_data(self, data):
        new_data = []
        for i in range(len(data)):
            if i % 2 == 0:
                new_data.append(data[i])
        return new_data

    def send_sensor_data_to_db(self, data):
        print("Sensors data sent to DB")
        self.sensor_repository.insert_sensor_values(data)

    def send_irrigation_data_to_db(self, data):
        print("Irrigation data sent to DB")
        self.irrigation_repository.insert_irrigation_values(data)


    def send_sensor_data_to_FIWARE(self, batch):
        fiware_batch = []
        for data in batch:
            for sensor in data["data"]:
                sensor_pos = str(sensor["x"]) + "_" + str(sensor["y"])
                sensor_value = sensor["v"]
                measurement_date = datetime.fromtimestamp(data["timestamp"]).strftime(fiware_api_datetime_format)
                output_data = self.build_fiware_sensor_update(sensor_pos, sensor_value, measurement_date)
                fiware_batch.append(output_data)
        print("Sensors data sent to FIWARE")
        self.send_to_FIWARE(fiware_batch)

    def send_irrigation_data_to_FIWARE(self, batch):
        fiware_batch = []
        for irrigation_data in batch:
            irrigation_data["timestamp"] = datetime.fromtimestamp(irrigation_data["timestamp"]).strftime(fiware_api_datetime_format)
            output_data = self.build_fiware_irrigation_update(irrigation_data)
            fiware_batch.append(output_data)
        print("Irrigation data sent to FIWARE")
        self.send_to_FIWARE(fiware_batch)

    def send_to_FIWARE(self, data):
        try:
            params = {"options": "keyValues"}
            update_body = {"actionType": "append", "entities": data}

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
        sensor_pos_to_fiware_ids = {
            "10_5" : "urn:ngsi-ld:Device:unibo:33b784aa-d8ed-444a-9da7-ab7e38a56fd4",
            "10_15" : "urn:ngsi-ld:Device:unibo:2f187cc9-265d-4750-888a-cc36066eba51",
            "10_25" : "urn:ngsi-ld:Device:unibo:7ac4e2e2-14cd-4394-975d-0beb6049b87f",
            "30_5" : "urn:ngsi-ld:Device:unibo:6fba17ce-4957-4aed-92e0-fc2543504bb7",
            "30_15" : "urn:ngsi-ld:Device:unibo:656abfa3-95f6-4af2-8dfa-4ad927d3d738",
            "30_25" : "urn:ngsi-ld:Device:unibo:9d9a9a02-6c5a-476a-9edf-067a18706bf4",
        }

        return {
            "id": sensor_pos_to_fiware_ids[sensor_pos],
            "name": f"Pinotech Soil Moisture {sensor_pos}",
            "description": "Researcher night simulation sensor",
            "type": "Device",
            "category": ["sensor"],
            "controlledProperty": ["soilMoisture"],
            "supportedUnits": ["P1"],
            "value": [f"{sensor_value}"],
            "refDeviceModel": "urn:ngsi-ld:DeviceModel:unibo:f757454d-66a4-41c5-8abf-a5848ab41191",
            "dateObserved": f"{measurement_date}",
            "location": {"type": "Point", "coordinates": [12.244149, 44.138811]},
        }

