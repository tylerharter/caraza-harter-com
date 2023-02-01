################################################################################
# Instructions:
# 1. Download canvas roster and save file as canvas.csv (in the local directory)
# 2. Run: "python3 canvas_to_roster.py" -> generates roster.json
# DO NOT PUSH roster.json / canvas.csv to gitlab! That will violate FERPA rules.
################################################################################


import os, sys, json, csv, random, re
from datetime import datetime

def main():
    print("canvas.csv => roster.json")
    
    # dummy roster.json file
    with open("roster.json", "w") as f:
        f.write("[]" + "\n") 
    
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
            lname, fname = row["Student"].split(", ")
            # add new students
            student_dict = {
                "fname": fname,
                "lname": lname,
                "name": row["Student"], 
                "email": email, 
                "net_id": net_id, 
                "section": section, 
                "enrolled": True}
            roster.append(student_dict)

    # anybody left here was not in canvas
    for key in roster_dict:
        # drop students
        roster_dict[key]["enrolled"] = False

    # parse roster
    with open("roster.json", "w") as f:
        json.dump(roster, f, indent=True, sort_keys=True)

if __name__ == '__main__':
    main()

