import os, sys, json

def main():
    if len(sys.argv) != 3:
        print("Usage: python exam_reminders.py <roster.json> <exam>")
        return

    with open(sys.argv[1]) as f:
        rows = json.load(f)

    emails = []
    for row in rows:
        if not row["enrolled"]:
            continue
        msg = 'Dear student, this is a friendly reminder that you have an exam coming up soon.  Details: {}.  Happy studying!'.format(row[sys.argv[2]])
        emails.append({
            'to':row['net_id']+'@wisc.edu',
            'subject': 'CS 301: Exam Time/Location Reminder',
            'message': msg
        })
    with open("emails.json", "w") as f:
        json.dump(emails, f, indent=2, sort_keys=True)

if __name__ == '__main__':
     main()
