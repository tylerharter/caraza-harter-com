import os, sys, json, csv, hashlib
from datetime import datetime


def md5(txt):
    a = hashlib.md5(txt.encode())
    b = a.hexdigest()
    return int(b, 16)


def get_alts():
    alts = {}
    with open('exam2alt.csv') as f:
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
    alts = get_alts()

    # section => rooms
    exams = {
        1: ['Monday, Apr 1 @ 7:15-9:15pm in Science Hall 180'],
        2: ['Monday, Apr 1 @ 7:15-9:15pm in Social Science 6210'],
        3: ['Monday, Apr 1 @ 7:15-9:15pm in Van Vleck B102',
            'Monday, Apr 1 @ 7:15-9:15pm in Van Vleck B130'],
    }

    with open('roster.json') as f:
        roster = json.load(f)

    for row in roster:
        if row['enrolled']:
            options = exams[row['section']]
            net_id = row['net_id']
            if net_id in alts:
                exam = alts[net_id]
            else:
                exam = options[md5(net_id) % len(options)]

            if row.get('exam2', None) != exam:
                print("%s: %s => %s" % (net_id, row.get('exam2', "none"), exam))
                row['exam2'] = exam
        else:
            row['exam2'] = None

    with open('roster.json', 'w') as f:
        json.dump(roster, f, sort_keys=True, indent=2)

if __name__ == '__main__':
     main()
