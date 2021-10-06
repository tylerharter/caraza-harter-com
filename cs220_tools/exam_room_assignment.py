import json
import sys

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


exam_name = sys.argv[1]

for student_dict in roster:
    if not student_dict['enrolled']:
        continue
    if(student_dict['section']) == 1:
        student_dict[exam_name] = "Psychology 105; 7:15 to 9:15 pm on Friday, October 8th"
        section1_count += 1        
    elif(student_dict['section']) == 2:
        student_dict[exam_name] = "Bascom 272; 7:15 to 9:15 pm on Friday, October 8th"
        section2_count += 1        
    elif(student_dict['section']) == 3:
        student_dict[exam_name] = "Humanities 3650; 7:15 to 9:15 pm on Friday, October 8th"
        section3_count += 1        
    elif(student_dict['section']) == 4:
        student_dict[exam_name] = "Ingraham B10; 7:15 to 9:15 pm on Friday, October 8th"
        section4_count += 1        
    elif(student_dict['section']) == 5:
        student_dict[exam_name] = "Online Honorlock exam; 24-hour window period from 3:00 PM (CST) on Friday, October 8th"
        section5_count += 1        

print("SEC001", section1_count)
print("SEC002", section2_count)
print("SEC003", section3_count)
print("SEC004", section4_count)
print("SEC005", section5_count)

write_json("../tools/exam1_roster.json", roster)
