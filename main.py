# Copyright 2025 Mia, Chiara
#
# Licensed under the AGPLv3.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/

# What this file should do? It should:
# 1. Start all the Sensors
# 2. Start the Webserver
# 3. Somehow transfer data from the Sensors to the Webserver

import subprocess

programs = [
    ["python", "sensors/lichtwiderstandsSensor.py"],
    ["python", "sensors/mikrofonSensor.py"],
    ["python", "sensors/temperaturSensor.py"]
]

# Start each one in parallel
processes = []
for prog in programs:
    p = subprocess.Popen(prog)
    processes.append(p)
