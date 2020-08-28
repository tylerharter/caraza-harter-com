import json, sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

print("sys.argv", sys.argv)
path = sys.argv[1]
print("READ DATA FROM", path)
data = read_json(path)
print("DATA", data)
print("TYPE", type(data))
print("SUM", sum(data))
