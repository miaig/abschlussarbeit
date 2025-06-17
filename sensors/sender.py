import socket
import json
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999

def send_data(data):
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        print(f"[+] Connected to server at {SERVER_HOST}:{SERVER_PORT}")
        message = json.dumps(data) + '\n'
        sock.sendall(message.encode('utf-8'))
    print("[x] Data sent and connection closed.")

# Test behavior if run directly
if __name__ == "__main__":
    test_data = {
        "location": "Building A - Lab 3",
        "sensors": [
            {
                "id": "sensor_001",
                "type": "temperature",
                "unit": "°C",
                "readings": [
                    { "ts": int(time.time()) - 60, "value": 22.3 },
                    { "ts": int(time.time()), "value": 22.8 }
                ]
            },
            {
                "id": "sensor_002",
                "type": "humidity",
                "unit": "%",
                "readings": [
                    { "ts": int(time.time()) - 60, "value": 45.2 },
                    { "ts": int(time.time()), "value": 46.1 }
                ]
            }
        ]
    }

    send_data(test_data)

    # Live Updates
    for i in range(15):
        live_update = {
            "location": "Building A - Lab 3",
            "sensors": [
                {
                    "id": "sensor_001",
                    "readings": [
                        { "ts": int(time.time()), "value": i }
                    ]
                },
                {
                    "id": "sensor_002",
                    "readings": [
                        { "ts": int(time.time()), "value": 23.0 + i }
                    ]
                }
            ]
        }
        send_data(live_update)
        time.sleep(2)

