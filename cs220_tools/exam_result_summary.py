import sys
import json
import boto3
import csv

################################################################################
# 1. Copy exam roster csv file (one used for exam check-in tool to cs220_tools
#    (ex: exam2_roster.csv)
# 2. Download exam result csv file and move to cs220_tools
#    (ex: exam1_results.csv)
# 3. Download canvas roster and save it as canvas.csv in cs220_tools
#
# Update below section on dropping question(s) if needed
#
# Sample execution:
# python3 exam_result_summary.py exam2_roster.csv exam2_results.csv exam2 "Exam2 (1379064)" "Exam 2: Honorlock (1389618)"
################################################################################

drop_flag = False
# KEY: exam version; VALUE: list of questions to drop / regrade
drop_questions = {
        "6": {"_10": "1"},
        "7": {"_20": "1"},
        "8": {"_10": "1"},
        "9": {"_25": "1"},
        }

roster_dict = {}
backup_roster = {}
netid_roster_dict = {}

BUCKET = 'caraza-harter-cs301'
s3 = boto3.client('s3')

# copied from https://automatetheboringstuff.com/2e/chapter16/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData


def convert_roster_to_netid_roster():
    for student_id in roster_dict:
        net_id = roster_dict[student_id]["netid"]
        roster_dict[student_id]["campus id"] = student_id
        netid_roster_dict[net_id] = roster_dict[student_id]

def read_roster(exam_roster):
    exam_roster_header = exam_roster[0]
    exam_roster = exam_roster[1:]
    for row in exam_roster:
        campus_id = row[exam_roster_header.index("id")]
        netid = row[exam_roster_header.index("login")]
        lname = row[exam_roster_header.index("lname")].lower().strip()
        fname = row[exam_roster_header.index("fname")].lower().strip()
        full_name = lname + "," + fname
        roster_dict[campus_id] = {
                "netid": netid,
                "lname": lname,
                "fname": fname
                }
        backup_roster[full_name] = {
                "campus id": campus_id,
                "netid": netid,
                "lname": lname,
                "fname": fname
        }

def read_exam_results(exam_results):
    exam_results_header = exam_results[0]
    exam_results = exam_results[1:]
    for row in exam_results:
        lname = row[exam_results_header.index("LastName")].lower().strip()
        fname = row[exam_results_header.index("FirstName")].lower().strip()
        campus_id = row[exam_results_header.index("ID")]
        special_codes = row[exam_results_header.index("SpecialCodes")].strip()
        print(special_codes.split(" "))
        codes = special_codes.split(" ")
        cleaned_codes = [code for code in codes if code != ""]
        if len(cleaned_codes) > 1:
            exam_version = cleaned_codes[1]
        else:
            exam_version = cleaned_codes[0]

        full_name = lname + "," + fname
        if campus_id not in roster_dict:
            # Initial check to filter out incorrect campus ID entries on the scantron
            # There will inevitably be some incorrect entries!
            if full_name in backup_roster:
                # Print this and send these students an email :)
                print("Wrong campus ID: ", end = "")
                print(backup_roster[full_name]["netid"] + "@wisc.edu")
                campus_id = backup_roster[full_name]["campus id"]
                roster_dict[campus_id] = backup_roster[full_name]
            else:
                # Good luck with the manual finding process ;)
                print("Couldn't find student: ", end = "")
                print(lname, fname, campus_id)
                #pass

        # Checks for questions which needs to be dropped
        # Gives points to students who chose different answer from
        # original answer option
        if drop_flag:
            drop = drop_questions[exam_version]
            for question in drop:
                student_answer = row[exam_results_header.index(question)]
                if student_answer != drop[question]:
                    roster_dict[campus_id]["total score"] = str(int(row[exam_results_header.index("TotalScore")]) + 1)
                else:
                    roster_dict[campus_id]["total score"] = row[exam_results_header.index("TotalScore")]
        else:
            #If all mappings work, this will populate dictionary with total score
            roster_dict[campus_id]["total score"] = row[exam_results_header.index("TotalScore")]

        #Marked answers from scantron
        answers = []
        for col_idx in range(7, 42):
            answers.append(row[col_idx])

        roster_dict[campus_id]["answers"] = answers

def gen_email(exam_name):
    emails = []
    for student_id in roster_dict:
        email = {
            "html":True, 
            "subject": "CS 220 - " + exam_name.upper() + " results", 
            "to": roster_dict[student_id]["netid"] + "@wisc.edu"
        }
        if "total score" not in roster_dict[student_id]:
            #print(email["to"])
            msg = '<p>Please see canvas for your exam score and answer choices, if you took exam via canvas quiz.</p>'
            msg += '<p>If you took an in-person exam, do not worry that you are seeing this message. It is likely that we missed retrieving your scantron - please email both Meena and Andy.</p>'
        else:
            #print(student_id, roster_dict[student_id])
            msg = '<p>Hello, your exam score was: ' + roster_dict[student_id]["total score"]
            msg += "<p>Your answers for each question:</p>"
            msg += "<ol>"
            for qnum in range(len(roster_dict[student_id]["answers"])):
                msg += "<li>" + roster_dict[student_id]["answers"][qnum] + "</li>"
            msg += "</ol>"
        
        email["message"] = msg
        emails.append(email)

    with open(exam_name + "_emails.json", "w") as f:
        json.dump(emails, f)


def update_canvas_score(exam_name, exam_column, exam_honorlock_column):
    canvas_data = process_csv("canvas.csv")
    header = canvas_data[0]
    canvas_data = canvas_data[1:]
    for row in canvas_data:
        if row[header.index(exam_honorlock_column)] != "N/A":
            row[header.index(exam_column)] = row[header.index(exam_honorlock_column)]
        else:
            net_id = row[header.index("SIS Login ID")].lower()
            net_id = net_id.replace("@wisc.edu", "")
            if net_id in netid_roster_dict:
                if "total score" in netid_roster_dict[net_id]:
                    row[header.index(exam_column)] = netid_roster_dict[net_id]["total score"]
                else:
                    row[header.index(exam_column)] = 0
            else:
                row[header.index(exam_column)] = 0

    canvas_data.insert(0, header)

    with open("canvas_" + exam_name + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(canvas_data)

def main():
    if len(sys.argv) < 6:
        print("""Usage: python {} <exam_roster.csv> <exam_results.csv> <exam name, 
        for ex: exam1> <exam column on canvas, for ex: Exam2 (1379064)>
        <honorlock exam column on canvas, for ex: Exam 2: Honorlock (1389618)>""".format(sys.argv[0]))
        sys.exit(1)

    exam_roster = process_csv(sys.argv[1])
    read_roster(exam_roster)

    exam_results = process_csv(sys.argv[2])
    read_exam_results(exam_results)

    exam_name = sys.argv[3]
    gen_email(exam_name)

    convert_roster_to_netid_roster()

    exam_column = sys.argv[4]
    exam_honorlock_column = sys.argv[5]
    update_canvas_score(exam_name, exam_column, exam_honorlock_column)

if __name__ == '__main__':
    main()
