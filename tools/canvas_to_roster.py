import os, sys, json, csv, random, re
from datetime import datetime

tas = []
with open("tas.json") as f:
    raw = json.load(f)
    for ta in raw:
        tas.extend([ta] * ta['weight'])
random.shuffle(tas)

def main():
    print("canvas.csv => roster.json")

    # parse roster
    with open("roster.json") as f:
        roster = json.load(f)

    roster_dict = {}
    for row in roster:
        net_id = row.get("net_id", "")
        if net_id != "":
            roster_dict[net_id] = row

    # parse canvas
    with open("canvas.csv") as f:
        canvas = [dict(row) for row in csv.DictReader(f)]

    # add students from canvas to roster
    ta_idx = 0
    for row in canvas:
        email = row.get("SIS Login ID", "").lower()
        section = None
        m = re.search(r'LEC00(\d)', row['Section'])
        if m:
            section = int(m.group(1))
        if email == "" or not email.endswith("@wisc.edu"):
            continue
        net_id = email.split("@")[0]

        if net_id in roster_dict:
            # update existing students
            roster_dict[net_id]["name"] = row["Student"]
            roster_dict[net_id]["section"] = section
            roster_dict[net_id]["enrolled"] = True
            roster_dict.pop(net_id)
        else:
            # add new students
            ta = tas[ta_idx % len(tas)]
            roster.append({"enrolled": True, "net_id": net_id, "section": section, "ta_name": ta["name"], "ta_email":ta["email"]})
            ta_idx += 1

    # anybody left here was not in canvas
    for key in roster_dict:
        # drop students
        roster_dict[key]["enrolled"] = False

    # parse roster
    with open("roster.json", "w") as f:
        json.dump(roster, f, indent=True, sort_keys=True)

if __name__ == '__main__':
    main()
