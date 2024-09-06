import requests
import pytz
from datetime import datetime

endpoint_url_update_entity = "http://137.204.70.156/v2/op/update:48082"
fiware_api_datetime_format = "%Y-%m-%dT%H:%M:%S"
timezone = pytz.timezone("Europe/Rome")

def build_fiware_update(sensor_pos, sensor_value, measurement_date):
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

sensor_pos = "10_5"
sensor_value = 50
measurement_date = datetime.now(tz=timezone).strftime(fiware_api_datetime_format)

try:
    data = build_fiware_update(sensor_pos, sensor_value, measurement_date)
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
