import os, sys, json, csv, hashlib, copy
from datetime import datetime

def main():
    with open("roster.json") as f:
        roster = json.load(f)

    exam = 'exam1'
    sections = {
        1: ["Fri Oct 4 @ 7:15pm in Bascom 272"],
        2: ["Fri Oct 4 @ 7:15pm in Humanities 3650", "Fri Oct 4 @ 7:15pm in Psychology 105"],
    }
    
    for row in roster:
        if row['enrolled']:
            selection = sections[row['section']][0]
            row[exam] = selection
            # rotate the one we just chose to the back
            sections[row['section']] = sections[row['section']][1:] + [selection]

    with open("roster.json", "w") as f:
        json.dump(roster, f, indent=2, sort_keys=True)

if __name__ == '__main__':
     main()
