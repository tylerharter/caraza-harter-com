import os, sys, json, csv
from datetime import datetime

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
    for row in canvas:
        email = row.get("SIS Login ID", "").lower()
        if email == "" or not email.endswith("@wisc.edu"):
            continue
        net_id = email.split("@")[0]

        if net_id in roster_dict:
            # update existing students
            roster_dict[net_id]["name"] = row["Student"]
            roster_dict[net_id]["enrolled"] = True
            roster_dict.pop(net_id)
        else:
            # add new students
            roster.append({"enrolled": True, "net_id": net_id, "ta": "tylerharter@gmail.com"})

    # anybody left here was not in canvas
    for key in roster_dict:
        if roster_dict[key].get("section", None) == 1:
            assert(datetime.today().year == 2019 and datetime.today().month <= 6)
            continue

        # drop students
        roster_dict[key]["enrolled"] = False

    # parse roster
    with open("roster.json", "w") as f:
        json.dump(roster, f, indent=True, sort_keys=True)
        
if __name__ == '__main__':
    main()
