import json
import sys

################################################################################
# roster.json is expected to be in ../tools/
# Writes updated roster to ../tools/exam<number>_roster.json
# alternate_netids file is expected to be in ../tools (just netids of students
# taking the alternate exam)
# mcburney_netids file is expected to be in ../tools (just netids of students
# taking the alternate exam)
# Check that and replace roster.json with that version
################################################################################

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

alternate_netIDs = {}
with open("../tools/alternate_netids") as FH:
    for line in FH:
        line = line.strip()
        if line not in alternate_netIDs:
            alternate_netIDs[line] = 1
        else:
            print("Duplicate (alternate):", line)

print("Number of alternate exam students:", len(alternate_netIDs))

mcburney_netIDs = {}
with open("../tools/mcburney_netids") as FH:
    for line in FH:
        line = line.strip()
        if line not in mcburney_netIDs:
            mcburney_netIDs[line] = 1
        else:
            print("Duplicate (mcburney):", line)

print("Number of McBurney students:", len(mcburney_netIDs))

roster = read_json("../tools/roster.json")
section1_count = 0
section2_count = 0
section3_count = 0
section4_count = 0
section5_count = 0

locations = {
    1: "Psychology 105; 7:15 to 9:15 pm on Wednesday, November 10th",
    2: "Bascom 272; 7:15 to 9:15 pm on Wednesday, November 10th",
    3: "Humanities 3650; 7:15 to 9:15 pm on Wednesday, November 10th",
    4: "Ingraham B10; 7:15 to 9:15 pm on Wednesday, November 10th",
    5: "Online Honorlock exam; 24-hour window period from 3:00 PM (CST) on Wednesday, November 10th",
    "alternate": "Ingraham 22; 7:15 to 9:15 pm on Thursday, November 11th",
    "mcburney": "Comp Sci 1325; 5:30 to 9:30 pm on Wednesday, November 10th",
}

section_counts = {}

if len(sys.argv) < 2:
    print("Usage: python3 {} <exam name, ex: exam1>".format(sys.argv[0]))
    sys.exit(1)

exam_name = sys.argv[1]

for student_dict in roster:
    if not student_dict['enrolled']:
        continue

    #Alternate exam
    if student_dict['net_id'] in alternate_netIDs:
        if student_dict['section'] == 5:
            print("Online section student filled alternate form:", student_dict['net_id'])
        alternate_netIDs[student_dict['net_id']] = 0
        student_dict[exam_name] = locations['alternate']
        if 'alternate' not in section_counts:
            section_counts['alternate'] = 0
        section_counts['alternate'] += 1
        continue
    
    # McBurney exam
    if student_dict['net_id'] in mcburney_netIDs:
        mcburney_netIDs[student_dict['net_id']] = 0
        student_dict[exam_name] = locations['mcburney']
        if 'mcburney' not in section_counts:
            section_counts['mcburney'] = 0
        section_counts['mcburney'] += 1
        continue


    #Regular exam
    if student_dict['section'] not in section_counts:
        section_counts[student_dict['section']] = 0
    section_counts[student_dict['section']] += 1
    
    student_dict[exam_name] = locations[student_dict['section']]

for section in section_counts:
    print("SEC00{} student count: {}".format(section, section_counts[section]))

write_json("../tools/{}_roster.json".format(exam_name), roster)

for netid, val in mcburney_netIDs.items():
    if val == 1:
        print(netid)
