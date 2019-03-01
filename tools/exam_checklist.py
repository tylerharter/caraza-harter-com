import os, sys, json, csv
from collections import defaultdict as ddict

EXAM = "exam1"

def main():
    if len(sys.argv) != 2:
        print("Usage: python exam_checklist.py <roster.json>")
        return

    groups = ddict(list)
    
    with open("roster.json") as f:
        rows = json.load(f)

    for row in rows:
        if not EXAM in row or row[EXAM] == None:
            continue
        groups[row[EXAM]].append("%s [%s in section %s]"
                                 % (row.get("name", "?"),
                                    row.get("net_id", "?"),
                                    str(row.get("section", "?"))))

    keys = sorted(groups.keys())

    with open("%s_checklist.csv" % EXAM, "w") as f:
        w = csv.writer(f)
        w.writerow(keys)
        i = 0
        while True:
            more = False
            row = []
            for k in keys:
                if i < len(groups[k]):
                    row.append(groups[k][i])
                    more = True
                else:
                    row.append("")
            if not more:
                break
            w.writerow(row)
            i += 1

if __name__ == '__main__':
     main()
