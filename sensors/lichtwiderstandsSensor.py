import time
import json
import os
import board
import digitalio

json_file = "json/ky018_data.json"
MAX_ENTRIES = 3000

light_pin = digitalio.DigitalInOut(board.D17)
light_pin.direction = digitalio.Direction.INPUT

dataldr = {
    "location": "Hausstrasse - 1",
    "id": "sensor_004",
    "type": "light",
    "unit": "bool", 
    "readings": []
}

def load_data():
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return dataldr.copy()

def save_data(data):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def capture_and_store(state):
    timestamp = int(time.time())
    data = load_data()

    data["readings"].append({"ts": timestamp,"value": state})

    if len(data["readings"]) > MAX_ENTRIES:
        data["readings"] = data["readings"][-MAX_ENTRIES:]

    save_data(data)

try:
    while True:
        if light_pin.value:
            light_state = True
        else:
            light_state = False

        print(f"Lichtzustand: {light_state}")
        capture_and_store(light_state)
        time.sleep(2)

except KeyboardInterrupt:
    print("Programm beendet.")
