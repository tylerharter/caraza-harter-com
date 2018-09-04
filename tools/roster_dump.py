#!/usr/bin/env python
import os, sys, csv, json

def student_iter():
    for section in [1, 2]:
        with open('/p/course/rosters/cs301-harter/cs301-00%d-000.csv' % section) as f:
            r = csv.DictReader(f)
            for row in r:
                row['lecture'] = section
                yield row

def main():
    students = list(student_iter())
    with open('roster.json', 'w') as f:
        f.write(json.dumps(students, indent=2))
    for student in students:
        print(student['campus_email'])

if __name__ == '__main__':
    main()
