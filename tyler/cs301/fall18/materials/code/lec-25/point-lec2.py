import json, sys

# read the data
path = 'points.json'
f = open(path)
data = f.read()
f.close()

# parse the data
print("RAW DATA:", data, "TYPE IS", type(data))
jdata = json.loads(data)
print("PARSED DATA:", jdata, "TYPE IS", type(jdata))

# give a point
name = sys.argv[1]
if not name in jdata:
    jdata[name] = 0
jdata[name] += 1
print("NEW DATA:", jdata, "TYPE IS", type(jdata))

# save result
fout = open(path, 'w')
data = fout.write(json.dumps(jdata))
fout.close()