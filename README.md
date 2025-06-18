# PiWebSense

## Git
This Repo gets pushed to three git hosts in the following order: 
 - [git.miaig.dev](https://git.miaig.dev/mia/abschlussarbeit)
 - [git.gay](https://git.gay/mia/abschlussarbeit)
 - [github.com](https://github.com/miaig/abschlussarbeit)

## Tech Stack / Hardware Requirements

- Raspberry Pi Model 4 for the sensors
- A Second Pc/Laptop/Server/Pi that'll host the Webserver
- **Programming languages used**: Python, jinja, HTML, CSS, JavaScript
- **Frameworks/tools/Libraries**:
  - Webserver:
    - flask
    - json
    - matplotlib
    - hashlib
    - socket
    - threading
    - os
    - datetime
  - Sensors:
    - datetime
    - time
    - json
    - os
    - board
    - adafruit_dht
    - digitalio
    - RPI.GPIO
    
- **Exxmple Sensors**:
  - LDR (Lightsensor)
  - Sound Detector
  - Temperature and humidity

## Docs

This Program aims to receive Data from a dynamic amount of Sensors and Display the data on the Webserver. This can be done using the example Sensors in the sensor folder or by just writing your own ones using the further down documented Json file. The server and port get defined in sensors/sender.py. That file can be imported as shown in the examples.

The Webserver distiguishes between two update formats: live and history.
The data needs to be providet in the following format to be considered a history update. To be considered a live update the fielts type and unit have to be removed from the transmission.

  ```Json
      {
      "location": "Building A - Lab 3",
      "sensors": [
        {
          "id": "sensor_001",
          "type": "temperature",
          "unit": "°C",
          "readings": [
            { "ts": 1747814400, "value": 22.5 },
            { "ts": 1747818000, "value": 23.0 },
            { "ts": 1747821600, "value": 23.7 }
          ]
        },
        {
          "id": "sensor_002",
          "type": "humidity",
          "unit": "%",
          "readings": [
            { "ts": 1747814400, "value": 45.2 },
            { "ts": 1747818000, "value": 47.1 },
            { "ts": 1747821600, "value": 46.8 }
          ]
        },
        {
          "id": "sensor_003",
          "type": "pressure",
          "unit": "hPa",
          "readings": [
            { "ts": 1747814400, "value": 1012.4 },
            { "ts": 1747818000, "value": 1012.8 },
            { "ts": 1747821600, "value": 1013.0 }
          ]
        }
      ]
    }
  ```

- `shell.nix`
  This file is only used for the nix packagemananger to set up a development environment for the Webserver only
- `.envrc`
  This is also a bit of linux nixos magic to automatically set up the development environment using direnv
- `main.py`
  This file starts all sensors at once for easy deployment at a site.

## Instalation

### Sensors
To Install the exmple Sensors, simply install all the Requiered packages mentioned further above 

## Acknowledgments

[Chiara](https://git.miaig.dev/chiara)
[Mia](https://git.miaig.dev/mia)

## License

PiWebSense
Copyright (C) 2025 Mia, Chiara

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License Version 3.0 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
