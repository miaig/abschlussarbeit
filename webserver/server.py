# Copyright 2025 Kieler, Chiara
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
            timestamps.append(i["readings"][j]["ts"])
            values.append(i["readings"][j]["value"])
        # print(i)
        # print(i["readings"][1])
        # print("\n")
        sensors[i["id"]] = Sensor(i["id"], i["unit"], i["type"], timestamps, values)
    f.close()


class Sensor:
    def __init__(self, id: str, unit: str, type: str, ts: list, value: list):
        self.id = id
        self.unit = unit
        self.type = type
        self.ts: list = ts
        self.values: list = value
        self.timeonly: list = []
        self.timedate: list = []
        for i in ts:
            # print(i)
            self.timeonly.append(datetime.fromtimestamp(int(i)).strftime("%H:%M.%S"))
            self.timedate.append(
                datetime.fromtimestamp(i).strftime("%d.%m.%Y %H:%M.%S")
            )

    def getId(self):
        return self.id

    def getUnit(self):
        return self.unit

    def getType(self):
        return self.type

    def getReadings(self, limit=5, reversed=True, timetype="ts"):
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
                    datadic[self.timedate[i]] = self.values[i]
            case _:
                return "ERROR: timetype must be one of 'ts', 'time', 'timedate'"
        return dict(sorted(datadic.items(), reverse=reversed))

    # This only exist because jinja2 can not accept arguments :(
    def getReadingsTimeDate(self):
        return self.getReadings(timetype="timedate")

    def getReadingsTime(self):
        return self.getReadings(timetype="time")

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


readJson()

# print("\n")
# print(sensors)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=sensors)


if __name__ == "__main__":
    app.run(debug=True)
