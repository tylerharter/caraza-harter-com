# Watch (Part 2)

IFRAME

# Practice

This constantly-updated JSON file shows the GPS location, speed, and
other info for every bus in Madison:
http://transitdata.cityofmadison.com/Vehicle/VehiclePositions.json

Paste and run the following to create a simplified version, `bus-simple.json` (no need to understand the code -- we just need that file for the next part):

```python
f = open("bus-simple.json", "w")
f.write("""
[
{"latitude":43.0748,"longitude":-89.3885,"bearing":90,"odometer":0,"speed":4.4704}
{"latitude":43.05375,"longitude":-89.46176,"bearing":270,"odometer":0,"speed":8.9408}
{"latitude":43.0531235,"longitude":-89.47349,"bearing":0,"odometer":0,"speed":0}
]
""")
f.close()
```

Now use the `read_json` function from lecture to read the file into a
list of dictionaries:

```python
import json

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc
    
buses = ????
buses
```

Add a line to the following snippet to accumulate all the speeds into
a list (which should then look like `[4.4704, 8.9408, 0]`).

```python
speeds = []
for bus in buses:
    print(bus)
    ????
speeds
```

# Questions About the Lecture?

Please ask below.
