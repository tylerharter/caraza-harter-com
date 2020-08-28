import json, sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# KEY: name, VAL: list of scores for that person
score_history_path = "score_history.json"
scores = read_json(score_history_path)

print("sys.argv", sys.argv)
name = sys.argv[1]
score = int(sys.argv[2])
if not name in scores:
    scores[name] = []
scores[name].append(score)

print(scores)
print("AVG", sum(scores[name]) / len(scores[name]))
write_json(score_history_path, scores)

