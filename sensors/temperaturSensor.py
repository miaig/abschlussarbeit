import time
import board
import adafruit_dht
import json
from datetime import datetime
import os

dhtDevice = adafruit_dht.DHT11(board.D23)

json_file = "json/ky015_data.json"

datatemp = {
     "location": "Hausstrasse - 3",
     "sensors": [
        {
            "id": "sensor_002",
            "type": "temperature",
            "unit": "°C",
            "readings": []
        },
        {
            "id": "sensor_003",
            "type": "humidity",
            "unit": "%",
            "readings": []
        }
    ]
}

def load_data():
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return datatemp.copy()

def save_data(data):
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

max_entries=3000

def capture_and_store(temperature_c,humidity):
    timestamp = int(time.time())
    data=load_data()

    temp_sensor = next(s for s in data["sensors"] if s["type"] == "temperature")
    hum_sensor = next(s for s in data["sensors"] if s["type"] == "humidity")

    temp_sensor["readings"].append({"ts": timestamp, "value": temperature_c})
    hum_sensor["readings"].append({"ts": timestamp, "value": humidity})

    if len(temp_sensor["readings"]) > max_entries:
        temp_sensor["readings"] = temp_sensor["readings"][-max_entries:]
    if len(hum_sensor["readings"]) > max_entries:
        hum_sensor["readings"] = hum_sensor["readings"][-max_entries:]

    save_data(data)


while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        timestamp = datetime.now().isoformat()
               
        if temperature_c is not None and humidity is not None:
            capture_and_store(temperature_c, humidity)
        else:
            print("Ungültige Messwerte.")
        
    except RuntimeError as error:
        print("Lese-Fehler:", error.args[0])
        dhtDevice.exit()
        time.sleep(3.0)
        dhtDevice=adafruit_dht.DHT11(board.D23)
        continue
    except KeyboardInterrupt:
        dhtDevice.exit()
        print("Beendet durch Benutzer.")
        break
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(3.0)
