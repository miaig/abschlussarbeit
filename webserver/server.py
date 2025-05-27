from datetime import datetime
import re
from flask import Flask, send_from_directory, render_template
import json
import matplotlib.pyplot as plt

# Global Variables:
jsonpath = "data.json"
htmldata = ""


# class Entries:
#     def __init__(self, id: str, ts: list, value: list):
#         self.id = id
#         templist: list = []
#         for i in range(len(ts)):
#             templist.append([ts[i], value[i]])
#         self.entries: list = templist
#
#     def printEntries(self):
#         print(self.entries)
#
#
# tese = Entries("sensor0", [1, 2, 3, 4], [10, 20, 30, 40])
# tese.printEntries()


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

    # def formatLine(self, ts: int):
    #     for i in self.ts:
    #         if i == ts:
    #             return f"{self.timedate}> {self.values[]}"


# Json
f = open(jsonpath)
jsondata = json.load(f)  # returns JSON object as a dictionary
# sensordict = dict()
sensors: dict = {}
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
    # sensordict[i["id"]] = [i["type"], i["unit"], i["readings"]]
    # print(sensordict[i["id"]])
    sensors[i["id"]] = Sensor(i["id"], i["unit"], i["type"], timestamps, values)


f.close()
print("\n")
# print(sensordict)
print(sensors)
# print(sensors["sensor_001"].getReadings(limit=2, reversed=True, timetype="time"))

# for i in sensordict:
#     type = sensordict[i][0]
#     unit = sensordict[i][1]
#     readings = ""
#     datapoints: list = []
#     sensorrange = len(sensordict[i][2]) if len(sensordict[i][2]) < 5 else 5
#     for j in range(sensorrange):
#         datapoints.append([])
#         ts = sensordict[i][2][j]["ts"]
#         value = sensordict[i][2][j]["value"]
#         datapoints[j].append(ts)
#         datapoints[j].append(value)
#         datapoints[j].append(unit)
#     datapoints.sort(reverse=True)
#
#     graphdata: list = [[], []]
#     for j in datapoints:
#         ts = j[0]
#         time = datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M.%S")
#         timeNoDate = datetime.fromtimestamp(ts).strftime("%H:%M.%S")
#         value = j[1]
#         unit = j[2]
#         # print(f"{time} {j}")
#         readings += f"{time}> {value}{unit}<br>"
#         graphdata[0].append(timeNoDate)
#         graphdata[1].append(value)
#
#     # create_plot(i, unit, graphdata[0], graphdata[1])
#
#     htmldata += f"""
#     <p>Id: {i}</p>
#     <p>Type: {type}</p>
#     <p>Readings:</p>
#     <div style="margin-left: 40px;">
#         {readings}
#         <img src="/plots/{i}.png" alt="Graph">
#     </div>
#     <hr>"""
#
# html = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <title>Sensor Data</title>
#         <style>
#             * {{
#                 font-family: 'Caskaydia Cove NF';
#                 font-size: 18px;
#                 color: white;
#                 background: #1C1C1C;
#             }}
#         </style>
#     </head>
#     <body>
#         {htmldata}
#     </body>
#     </html>
# """


# class MyHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         # self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(html.encode("utf-8"))
#
#
# if __name__ == "__main__":
#     server_address = ("", 8000)
#     httpd = HTTPServer(server_address, MyHandler)
#     print("Serving on http://localhost:8000")
#     httpd.serve_forever()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=sensors)


# @app.before_request
# def before_request():
#     for sensor in sensors.values():
#         print(sensor)
#         sensor.renderPlot()


if __name__ == "__main__":
    app.run(debug=True)
