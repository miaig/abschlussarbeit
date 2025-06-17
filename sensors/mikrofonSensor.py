import RPi.GPIO as GPIO
import time
import json
from datetime import datetime
import os

SENSOR_PIN = 17
JSON_FILE = "json/ky037_data.json"
INTERVAL = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)


datamikro = {
    "location": "Hausstrasse - 2",
    "id": "sensor_001",
    "type": "noise",
    "unit": "bool",
    "readings": []
}

def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return datamikro.copy()

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def capture_and_store():
    state = GPIO.input(SENSOR_PIN)
    timestamp = int(time.time())
    noise = True if state == 0 else False

    entry = { "ts": timestamp, "value": noise}

    data = load_data()
    data["readings"].append(entry)
    save_data(data)

    dt_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{dt_str}] Noise detected: {'YES' if noise else 'NO'}")

if __name__ == "__main__":
    print("Starting noise detection with KY-037")
    try:
        while True:
            capture_and_store()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        GPIO.cleanup()
