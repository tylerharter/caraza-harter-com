import os, sys, json, csv, hashlib, copy
from datetime import datetime


def md5(txt):
    a = hashlib.md5(txt.encode())
    b = a.hexdigest()
    return int(b, 16)


def get_alts():
    alts = {}
    with open('exam3alt.csv') as f:
        r = csv.DictReader(f)
        for row in r:
            for k,v in row.items():
                net_id = v.split('@')[0].lower().strip()
                if not net_id:
                    continue
                if net_id in alts:
                    print("Duplicate!", net_id)
                alts[net_id] = k
    return alts


def main():
    exam_name = "final"
    
    # open-seats is half the room capicity (to support every-other seating)
    venue1 = {'name': 'Wednesday, May 8th @ 7:45am in Psych 113', 'open-seats': 999}
    venue2 = {'name': 'Wednesday, May 8th @ 7:45am in Soc Sci 6210', 'open-seats': 230}
    venue3 = {'name': 'Wednesday, May 8th @ 7:45am in Van Vleck B102', 'open-seats': 163}

    # section => venue
    exams = {
        1: [venue1],
        2: [venue2],
        3: [venue2, venue3],
    }

    with open('roster.json') as f:
        roster = json.load(f)
    orig = copy.deepcopy(roster)

    # get view of enrolled students in an arbitrary (but sorted) order
    enrolled = [row for row in roster if row['enrolled']]
    enrolled.sort(key=lambda row: md5(row['net_id']))

    # STEP 1: assign based on section and remaining seats
    for section in [1, 2, 3]:
        for row in enrolled:
            if row['section'] != section:
                continue
            net_id = row['net_id']
            venues = exams[row['section']]
            chosen = None
            for v in venues:
                if v["open-seats"] > 0:
                    chosen = v
                    break
            assert(chosen)
            row[exam_name] = chosen["name"]
            chosen["open-seats"] -= 1

    # STEP 2: record overrides
    alts = get_alts()
    for row in enrolled:
        net_id = row['net_id']
        if net_id in alts:
            row[exam_name] = alts[net_id]

    # diff orig and roster
    for before, after in zip(orig, roster):
        if before != after:
            print(before["net_id"])
            for k in set(before.keys())|set(after.keys()):
                v1 = before.get(k,None)
                v2 = after.get(k, None)
                if v1 != v2:
                    print("  %s => %s" % (str(v1), str(v2)))


    with open('roster.json', 'w') as f:
        json.dump(roster, f, sort_keys=True, indent=2)

if __name__ == '__main__':
     main()
