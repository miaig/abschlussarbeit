# Copyright 2025 Mia, Chiara
#
# Licensed under the AGPLv3.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/


from datetime import datetime
from flask import Flask, render_template
import json
import matplotlib
import hashlib
import socket
import threading
import os
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Global Variables:
jsonpath = "data_big.json"
sensors: dict = {}


def readJson():
    f = open(jsonpath)
    jsondata = json.load(f)  # returns JSON object as a dictionary
    for i in jsondata["sensors"]:  # Iterating through the json list
        timestamps: list = []
        values: list = []
        # print(len(i["readings"]))
        for j in range(len(i["readings"])):
            timestamps.insert(0, i["readings"][j]["ts"])
            values.insert(0, i["readings"][j]["value"])
        # print(i)
        # print(i["readings"][1])
        # print("\n")
        sensors[(jsondata["location"], i["id"])] = Sensor(i["id"], i["unit"], i["type"], timestamps, values)
    f.close()


def handle_connection(conn, addr):
    print(f"[+] Connected from {addr}")
    buffer = ""
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break  # client closed connection
            buffer += data.decode("utf-8")

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    try:
                        message = json.loads(line)
                        process_message(message)
                    except json.JSONDecodeError:
                        print("[!] Invalid JSON")
    finally:
        conn.close()
        print(f"[-] Disconnected from {addr}")

def process_message(message):
    location = message.get("location", "unknown_location")
    for s in message.get("sensors", []):
        sensor_id = s["id"]
        key = (location, sensor_id)

        # Check if this is a new sensor (history), or just live data
        if "type" in s and "unit" in s:
            # Full metadata available
            timestamps = [r["ts"] for r in s["readings"]]
            values = [r["value"] for r in s["readings"]]
            sensors[key] = Sensor(sensor_id, s["unit"], s["type"], timestamps, values)
        else:
            # Live update, assume sensor already exists
            if key not in sensors:
                print(f"[!] Live data received for unknown sensor {key}, ignoring.")
                continue

            sensor = sensors[key]
            for reading in s.get("readings", []):
                sensor.ts.insert(0, reading["ts"])
                sensor.timeonly.insert(0, datetime.fromtimestamp(int(reading["ts"])).strftime("%H:%M.%S"))
                sensor.timedate.insert(0, datetime.fromtimestamp(int(reading["ts"])).strftime("%d.%m.%Y %H:%M.%S"))
                sensor.values.insert(0, reading["value"])


class Sensor:
    def __init__(self, id: str, unit: str, type: str, ts: list, value: list):
        self.id = id
        self.unit = unit
        self.type = type
        self.ts: list = ts
        self.values: list = value
        self.timeonly: list = []
        self.timedate: list = []
        self.hash = hashlib.sha256(repr(ts).encode()).hexdigest()
        for i in ts:
            # print(i)
            self.timeonly.insert(0, datetime.fromtimestamp(int(i)).strftime("%H:%M.%S"))
            self.timedate.insert(0, datetime.fromtimestamp(i).strftime("%d.%m.%Y %H:%M.%S"))

    def getId(self):
        return self.id

    def getUnit(self):
        return self.unit

    def getType(self):
        return self.type

    def getReadings(self, limit=10, reversed=True, timetype="ts"):
        limit += 1
        datadic: dict = {}
        match timetype:
            case "ts":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    datadic[self.ts[i]] = self.values[i]
            case "time":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    datadic[self.timeonly[i]] = self.values[i]
            case "timedate":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    # print(i)
                    # print(self.values[i])
                    datadic[self.timedate[i]] = self.values[i]
            case _:
                return "ERROR: timetype must be one of 'ts', 'time', 'timedate'"
        return dict(sorted(datadic.items(), reverse=reversed))

    # This only exist because jinja2 can not accept arguments :(
    def getReadingsTimeDate(self):
        return self.getReadings(timetype="timedate")

    def getReadingsTime(self):
        return self.getReadings(timetype="time")

    def getChartJSData(self, limit=10, reversed=False, timetype="ts"):
        limit += 1
        datalist: list = [[],[]]
        match timetype:
            case "ts":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    datalist[0].append(self.ts[i])
                    datalist[1].append(self.values[i])
            case "time":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    datalist[0].append(self.timeonly[i])
                    datalist[1].append(self.values[i])
            case "timedate":
                for i in range(limit if limit < len(self.ts) else len(self.ts)):
                    datalist[0].append(self.timedate[i])
                    datalist[1].append(self.values[i])
            case _:
                return "ERROR: timetype must be one of 'ts', 'time', 'timedate'"
        if not reversed:
            datalist[0].reverse()
            datalist[1].reverse()
        return datalist


    def getValueByTimestamp(self, ts: int):
        c = 0
        for i in self.ts:
            c += 1
            if i == ts:
                return self.values[c]

    def getTimestampByValue(self, value: float):
        values: list = []
        for i in range(len(self.values)):
            if self.values[i] == value:
                values.append(self.ts[i])
        return values

    def renderPlot(self):
        plt.plot(self.timeonly, self.values)
        plt.title(self.id)
        plt.xlabel("Time")
        plt.ylabel(self.unit)
        path = f"plots/{self.id}.png"
        plt.savefig(f"static/{path}")  # Save to file
        plt.close()
        return path

    def getHash(self):
        return self.hash


def start_socket_server(host='0.0.0.0', port=9999):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[*] Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

# if __name__ == "__main__":
#     start_server()


# readJson()

# print("\n")
# print(sensors)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=sensors)

# @app.before_request
# def reload_data():
#     readJson()
#     print("hello")

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=start_socket_server, daemon=True).start()
    app.run(debug=True)
