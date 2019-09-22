import os, sys, json, csv


def get_alts(path):
    alts = {}
    with open(path) as f:
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
    if len(sys.argv) != 3:
        print("Usage: python3 alt_to_roster.py <exam-name> <path-to-csv>")
        return
    exam, path = sys.argv[1:]

    alts = get_alts(path)

    with open("roster.json") as f:
        roster = json.load(f)

    for row in roster:
        if row['enrolled']:
            email = row['net_id']
            if email in alts:
                if row[exam] != alts[email]:
                    print("BEFORE", row)
                    row[exam] = alts[email]
                    print("AFTER", row)

    with open('roster.json', 'w') as f:
        json.dump(roster, f, sort_keys=True, indent=2)

if __name__ == '__main__':
     main()
