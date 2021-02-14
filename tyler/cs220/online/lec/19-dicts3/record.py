import json, sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
# READ previous records
# key: player name, val: a list of their scores
scores = read_json("scores.json")

# UPDATE records
name = sys.argv[1]
score = int(sys.argv[2])
if not name in scores:
    scores[name] = []
scores[name].append(score)
player_scores = scores[name]
print("AVG:", sum(player_scores) / len(player_scores))

# WRITE new records
write_json("scores.json", scores)