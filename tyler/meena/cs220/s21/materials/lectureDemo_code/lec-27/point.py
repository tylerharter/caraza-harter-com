import sys
import json
import os

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

playerName = sys.argv[1]
dataFile = "point.json"
data = {}

#Check if "point.json" exists, if so load data from it
if os.path.exists(dataFile):
    data = read_json(dataFile)
    #Check if player is a known player
    if playerName in data:
        data[playerName] += 1
    else:
        data[playerName] = 1
    write_json(dataFile, data)
else:
    data[playerName] = 1
    write_json(dataFile, data)

for player in data:
    print(player + ":", str(data[player]))
