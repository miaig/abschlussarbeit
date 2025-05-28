import time
import json
import os
import board
import digitalio

json_file = "ky018_data.json"
MAX_ENTRIES = 3000

light_pin = digitalio.DigitalInOut(board.D17)
light_pin.direction = digitalio.Direction.INPUT

data_template = {
    "id": "sensor_004",
    "type": "light",
    "unit": "state", 
    "reading": []
}

def load_data():
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return data_template.copy()

def save_data(data):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def capture_and_store(state):
    timestamp = int(time.time())
    data = load_data()

    data["reading"].append({
        "ts": timestamp,
        "state": state
    })

    if len(data["reading"]) > MAX_ENTRIES:
        data["reading"] = data["reading"][-MAX_ENTRIES:]

    save_data(data)

try:
    while True:
        if light_pin.value:
            light_state = "hell"
        else:
            light_state = "dunkel"

        print(f"Lichtzustand: {light_state}")
        capture_and_store(light_state)
        time.sleep(2)

except KeyboardInterrupt:
    print("Programm beendet.")