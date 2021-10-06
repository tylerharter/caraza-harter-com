import json
import sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

roster = read_json("../tools/roster.json")

alternate_netIDs = {}
with open("../tools/alternate.txt") as FH:
    for line in FH:
        line = line.strip()
        if line not in alternate_netIDs:
            alternate_netIDs[line] = 1
        else:
            print("Duplicate:", line)

print(len(alternate_netIDs))

exam_name = sys.argv[1]

count = 0
for student_dict in roster:
    #if not student_dict['enrolled']:
    #    continue
    if(student_dict['net_id']) in alternate_netIDs:
        if not student_dict['enrolled']:
            print("Strange:", student_dict)
        count += 1
        student_dict[exam_name] = "Location: TBD; 7:15 to 9:15 pm on Tuesday, October 12th"

print(count)

write_json("../tools/exam1_roster.json", roster)
