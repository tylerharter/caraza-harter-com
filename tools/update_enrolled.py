import os, sys, csv, json, re

def main():
    if len(sys.argv) != 3:
        print('Usage: python update_enrolled.py <canvas.csv> <roster.json>')
        return

    emails = []
    net_ids = []
    sections = {}

    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)

        for row in reader:
            email = row['SIS Login ID'].lower()
            emails.append(email)
            if email.split('@')[-1] == 'wisc.edu':
                net_id = email.split('@')[0]
                net_ids.append(net_id)
                m = re.search(r'LEC00(\d)', row["Section"])
                assert(m)
                sections[net_id] = int(m.group(1))
    net_ids = set(net_ids)
    print(len(net_ids))

    with open(sys.argv[2]) as f:
        roster = json.load(f)
    for row in roster:
        net_id = row['net_id']
        if net_id in net_ids:
            row['enrolled'] = True
            row['section'] = sections[net_id]
        else:
            row['enrolled'] = False
            row['section'] = None

    with open(sys.argv[2], 'w') as f:
        json.dump(roster, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
