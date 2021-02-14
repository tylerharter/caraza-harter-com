import json, sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

    
filename = sys.argv[1]
nums = read_json(filename)
print(sum(nums))