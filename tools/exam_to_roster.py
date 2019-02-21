import os, sys, json

def main():
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
            exam = options[hash(row['net_id']) % len(options)]
            row['exam1'] = exam
        else:
            row['exam1'] = None

    with open('roster2.json', 'w') as f:
        json.dump(roster, f, sort_keys=True, indent=2)

if __name__ == '__main__':
     main()
