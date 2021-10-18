import json
import sys

################################################################################
# roster.json is expected to be in ../tools/
# Writes updated roster to ../tools/exam<number>_roster.json
# Check that and replace roster.json with that version
# TODO: Before exam2 update this script to directly handle alternate and
# McBurney exams
################################################################################

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

roster = read_json("../tools/roster.json")
section1_count = 0
section2_count = 0
section3_count = 0
section4_count = 0
section5_count = 0

locations = {
    1: "Psychology 105; 7:15 to 9:15 pm on Friday, October 8th",
    2: "Bascom 272; 7:15 to 9:15 pm on Friday, October 8th",
    3: "Humanities 3650; 7:15 to 9:15 pm on Friday, October 8th",
    4: "Ingraham B10; 7:15 to 9:15 pm on Friday, October 8th",
    5: "Online Honorlock exam; 24-hour window period from 3:00 PM (CST) on Friday, October 8th"
}

section_counts = {}

if len(sys.argv) < 2:
    print("Usage: python3 {} <exam name, ex: exam1>".format(sys.argv[0]))
    sys.exit(1)

exam_name = sys.argv[1]

for student_dict in roster:
    if not student_dict['enrolled']:
        continue
    if student_dict['section'] not in section_counts:
        section_counts[student_dict['section']] = 0
    else:
        section_counts[student_dict['section']] += 1
    
    student_dict[exam_name] = locations[student_dict['section']]

for section in section_counts:
    print("SEC00{} student count: {}".format(section, section_counts[section]))

write_json("../tools/{}_roster.json".format(exam_name), roster)
