import os, sys, csv, json

def main():
    if len(sys.argv) != 3:
        print('Usage: python update_enrolled.py canvas.csv roster.json')

    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        emails = (row['SIS Login ID'].lower() for row in reader)
        net_ids = [email.split('@')[0] for email in emails if email.split('@')[-1] == 'wisc.edu']
    net_ids = set(net_ids)
    print(len(net_ids))

    with open(sys.argv[2]) as f:
        roster = json.load(f)
    for row in roster:
        row['enrolled'] = row['net_id'] in net_ids

    with open(sys.argv[2], 'w') as f:
        json.dump(roster, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
