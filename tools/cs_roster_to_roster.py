import os, sys, json, csv, random, re
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: cs_roster_to_roste.py <cs-roster1.csv> [<cs-roster2.csv> ...]")

    # KEY: netID, VAL: Campus ID
    campus_ids = {}
    for p in sys.argv[1:]:
        with open(p) as f:
            r = csv.DictReader(f)
            for row in r:
                campus_ids[row["netid"].lower()] = row["isis_univid"]

    # parse roster
    with open("roster.json") as f:
        roster = json.load(f)

    for row in roster:
        if row["enrolled"]:
            if row["net_id"] in campus_ids:
                row["campus_id"] = campus_ids[row["net_id"]]
            else:
                print("Cannot find campus ID: ", row)

    # parse roster
    with open("roster.json", "w") as f:
        json.dump(roster, f, indent=True, sort_keys=True)

if __name__ == '__main__':
    main()
