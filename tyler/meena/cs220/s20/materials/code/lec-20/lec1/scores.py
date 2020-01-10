import json, sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc
    
# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

scores = read_json("scores.json")
name = sys.argv[1]
new_score = sys.argv[2]
scores[name] = new_score
write_json("scores.json", scores)
print("Curr high scores: ", scores)
