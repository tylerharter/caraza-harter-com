import os, sys, json, csv, hashlib
from datetime import datetime


def md5(txt):
    a = hashlib.md5(txt.encode())
    b = a.hexdigest()
    return int(b, 16)


def get_alts():
    alts = {}
    with open('exam1alt.csv') as f:
        r = csv.DictReader(f)
        for row in r:
            for k,v in row.items():
                alts[v.split('@')[0].lower().strip()] = k
    return alts


def main():
    alts = get_alts()

    # section => rooms
    exams = {
        1: ['Monday, Feb 25 @ 7:15-9:15pm in Science Hall 180'],
        2: ['Monday, Feb 25 @ 7:15-9:15pm in Social Science 6210'],
        3: ['Monday, Feb 25 @ 7:15-9:15pm in Van Vleck B102',
            'Monday, Feb 25 @ 7:15-9:15pm in Van Vleck B130'],
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

            if row['exam1'] != exam:
                if "Van Vleck" in row['exam1'] and "Van Vleck" in exam:
                    # hack because dealing with Python hash() not being deterministic
                    assert(datetime.today().year == 2019 and datetime.today().month == 2)
                    continue

                print("%s: %s => %s" % (net_id, row['exam1'], exam))
                row['exam1'] = exam
        else:
            row['exam1'] = None

    with open('roster.json', 'w') as f:
        json.dump(roster, f, sort_keys=True, indent=2)

if __name__ == '__main__':
     main()
