from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Opening JSON file
f = open("data.json")

# returns JSON object as a dictionary
data = json.load(f)
sensors = dict()
sensorid = None
sensortype = None
sensorunit = None
sensorreadings = None
readings = None

# Iterating through the json list
for i in data["sensors"]:
    sensorid = i["id"]
    sensors[sensorid] = [i["type"], i["unit"], i["readings"]]
    # if i["type"] == "temperature":
    #     readings = i["readings"]


# Closing file
f.close()

html = ""

for i in sensors:
    type = sensors[i][0]
    unit = sensors[i][1]
    readings = f"{sensors[i][2][0]["ts"]}: {sensors[i][2][0]["value"]} {unit}"
    html += f"""
    <p>Id: {i}</p>
    <p>Type: {type}</p>
    <p>Readings: {readings}</p>
    <p>---------------------------------------------</p>
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
