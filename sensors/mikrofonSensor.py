import RPi.GPIO as GPIO
import time
import json
from datetime import datetime
import os

SENSOR_PIN = 17
JSON_FILE = "ky037_data.json"
INTERVAL = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)


SENSOR_INFO = {
    "id": "sensor_001",
    "type": "noise",  # Geräuschsensor
    "unit": "bool",   # 1 oder 0 (geräusch ja/nein)
    "readings": []
}

def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return SENSOR_INFO.copy()  # frisches Grundgerüst

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def capture_and_store():
    state = GPIO.input(SENSOR_PIN)
    timestamp = int(time.time())  # Unix-Zeitstempel (int)
    noise = 1 if state == 0 else 0

    entry = {
        "ts": timestamp,
        "value": noise
    }

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