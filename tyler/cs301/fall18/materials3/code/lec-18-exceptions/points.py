import sys
import json

try:
    fr = open('points.json')
    scores = json.load(fr)
    fr.close()
except:
    scores = {}


try:
    fw = open('points.json', "w")
    name = sys.argv[1]
    if name in scores:
        scores[name] += 1
    else:
        scores[name] = 1
    json.dump(scores, fw, indent=4)
    print(scores)
    fw.close()

except Exception as e:
    print("Exception:", e)

