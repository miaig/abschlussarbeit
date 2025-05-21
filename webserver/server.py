from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json

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

htmldata = ""

for i in sensors:
    type = sensors[i][0]
    unit = sensors[i][1]
    readings = ""
    sensorrange = len(sensors[i][2]) if len(sensors[i][2]) < 5 else 4
    for j in range(sensorrange):
        ts = sensors[i][2][j]["ts"]
        time = datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M.%S")
        value = sensors[i][2][j]["value"]
        readings += f"{time}: {value}{unit}<br>"
    htmldata += f"""
    <p>Id: {i}</p>
    <p>Type: {type}</p>
    <p>Readings:</p>
    <div style="margin-left: 40px;">
        {readings}
    </div>
    <p>---------------------------------------------</p>
    """

html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sensor Data</title>
        <style>
            * {{
                font-family: 'Times New Roman';
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
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Serving on http://localhost:8000")
    httpd.serve_forever()
