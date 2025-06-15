import time
import board
import adafruit_dht
import json
from datetime import datetime
import os

dhtDevice = adafruit_dht.DHT11(board.D23)

json_file = "json/ky015_data.json"

datatemphum = {
    "id": "sensor_002/3",
    "type": "environment",
    "unit": {
         "temperature": "°C",
         "humidity": "%"
    },
    "reading": []
}


def load_data():
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return datatemphum.copy()

def save_data(data):
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

max_entries=3000

def capture_and_store(temperature_c,humidity):
    timestamp = int(time.time())

    data = load_data()
    data["reading"].append({
           "ts": timestamp,
           "temperature": temperature_c,
           "humidity":humidity
    })


    if len(data["reading"]) > max_entries:
        data["reading"] = data["reading"][-max_entries:]

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
