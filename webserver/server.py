from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import matplotlib.pyplot as plt
import mimetypes

mimetypes.add_type("image/png", ".png")

# Opening JSON file
f = open("data.json")

# returns JSON object as a dictionary
data = json.load(f)
sensors = dict()

# Iterating through the json list
for i in data["sensors"]:
    sensors[i["id"]] = [i["type"], i["unit"], i["readings"]]

# Closing file
f.close()


def create_plot(id: str, unit: str, xaxis: list, yaxis: list):
    plt.plot(xaxis, yaxis)
    plt.title(id)
    plt.xlabel("Time")
    plt.ylabel(unit)
    plt.savefig(f"plots/{id}.png")  # Save to file
    plt.close()


htmldata = ""


def sortfunc(körber):
    return körber


for i in sensors:
    type = sensors[i][0]
    unit = sensors[i][1]
    readings = ""
    datapoints: list = []
    sensorrange = len(sensors[i][2]) if len(sensors[i][2]) < 5 else 5
    for j in range(sensorrange):
        datapoints.append([])
        ts = sensors[i][2][j]["ts"]
        value = sensors[i][2][j]["value"]
        datapoints[j].append(ts)
        datapoints[j].append(value)
        datapoints[j].append(unit)
    datapoints.sort(key=sortfunc, reverse=True)

    graphdata: list = [[], []]
    for j in datapoints:
        ts = j[0]
        time = datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M.%S")
        timeNoDate = datetime.fromtimestamp(ts).strftime("%H:%M.%S")
        value = j[1]
        unit = j[2]
        # print(f"{time} {j}")
        readings += f"{time}> {value}{unit}<br>"
        graphdata[0].append(timeNoDate)
        graphdata[1].append(value)

    create_plot(i, unit, graphdata[0], graphdata[1])

    htmldata += f"""
    <p>Id: {i}</p>
    <p>Type: {type}</p>
    <p>Readings:</p>
    <div style="margin-left: 40px;">
        {readings}
        <img src="/plots/{i}.png" alt="Graph">
    </div>
    <hr>
    """

html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sensor Data</title>
        <style>
            * {{
                font-family: 'Caskaydia Cove NF';
                font-size: 18px;
                color: white;
                background: #1C1C1C;
            }}
        </style>
    </head>
    <body>
        {htmldata}
    </body>
    </html>
"""


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Serving on http://localhost:8000")
    httpd.serve_forever()
