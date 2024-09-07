import requests
from repository.repository import Repository
from time import sleep

from datetime import datetime
fiware_api_datetime_format = "%Y-%m-%dT%H:%M:%S"

class DataController:

    def update_dbs(self):    
        self.repository = Repository()
        # rimuovere!!
        sleep(2)
        while True:
            last_sensor_data = self.data_collector.get_all_sensor_data_with_interpolation()[:2]
            if(last_sensor_data != None and len(last_sensor_data) > 0):
                self.send_data_to_server(last_sensor_data)
                self.send_data_to_orion(last_sensor_data)                
            sleep(60)

    def __init__(self, data_collector):
        self.data_collector = data_collector
        

    def send_data_to_server(self, data):
        self.repository.insert_sensor_values(data)        

    def send_data_to_orion(self, batch):
        for data in batch:
            for sensor in data["data"]:
                sensor_pos = str(sensor["x"]) + "_" + str(sensor["y"])
                sensor_value = sensor["v"]
                measurement_date = datetime.fromtimestamp(data["timestamp"]).strftime(fiware_api_datetime_format)
                output_data = self.build_fiware_update(sensor_pos, sensor_value, measurement_date)
                print(output_data)
        # try:
        #     data = build_fiware_update(sensor_pos, sensor_value, measurement_date)
        #     params = {"options": "keyValues"}
        #     update_body = {"actionType": "append", "entities": [data]}

        #     response = requests.post(
        #         endpoint_url_update_entity, params=params, json=update_body
        #     )

        #     response.raise_for_status()

        #     if response.status_code >= 200 and response.status_code < 300:
        #         print("Successfully updated FIWARE entity")

        # except Exception as e:
        #     print(e)
        #     print(e.__doc__)

    def build_fiware_update(self, sensor_pos, sensor_value, measurement_date):
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