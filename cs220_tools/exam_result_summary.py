import os, sys, json, math, datetime, boto3
from collections import defaultdict as ddict

import csv
# copied from https://automatetheboringstuff.com/2e/chapter16/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

roster_dict = {}
backup_roster = {}
netid_roster_dict = {}

BUCKET = 'caraza-harter-cs301'
s3 = boto3.client('s3')

TEST_NET_IDS = []

LATE_DAY_ALLOCATION = 9

def gen_html(prows, include_intro=True):
    cum_late = 0

    intro = """<p>
    Dear Student,
    </p>

    <p>Here is your project summary, as of Mar 12 2020:</p>
    """

    if include_intro:
        html = intro.split('\n')
    else:
        html = ['<h1>']

    for p in prows:
        html.append('<h2>' + p['project'].upper() + '</h2>')
        html.append('<ul>')
        line = '<li>Feedback: <a href="{}">{} reviewer comments</a>'
        html.append(line.format(p['code_review_url'], p['comment_count']))
        html.append('<li>Score: ' + str(p['score']))
        if p.get('override', False):
            html[-1] += ' [override]'
        html.append('<li>Days Late: ' + str(p['late_days']))

        # handle late days
        cum_late += p['late_days']
        if (cum_late > LATE_DAY_ALLOCATION and p['late_days'] > 0):
            print('dropping projects because late!')
            html.append("<li>WARNING: late days exhausted ({} used to this point). ".format(cum_late) +
                        "This won't be counted. "+
                        "Please email your instructor to discuss.")

        html.append('</ul>')
    return '\n'.join(html)

def convert_roster_to_netid_roster():
    for student_id in roster_dict:
        net_id = roster_dict[student_id]["netid"]
        roster_dict[student_id]["campus id"] = student_id
        netid_roster_dict[net_id] = roster_dict[student_id]

def read_roster(exam_roster):
    exam_roster_header = exam_roster[0]
    exam_roster = exam_roster[1:]
    for row in exam_roster:
        campus_id = row[0]
        netid = row[3]
        lname = row[4].lower().strip()
        fname = row[5].lower().strip()
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
        lname = row[0].lower().strip()
        fname = row[1].lower().strip()
        campus_id = row[3]
        full_name = lname + "," + fname
        if campus_id not in roster_dict:
            # Initial check to filter out incorrect campus ID entries on the scantron
            # There will inevitably be some incorrect entries!
            if full_name in backup_roster:
                # Print this and send these students an email :)
                # print(backup_roster[full_name]["netid"] + "@wisc.edu")
                campus_id = backup_roster[full_name]["campus id"]
                roster_dict[campus_id] = backup_roster[full_name]
            else:
                # Good luck with the manual finding process ;)
                # print(lname, fname, campus_id)
                pass

        #If all mappings work, this will populate dictionary with total score
        roster_dict[campus_id]["total score"] = row[5]
        
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
            "subject": "CS 220 - Exam 1 results", 
            "to": roster_dict[student_id]["netid"] + "@wisc.edu"
        }
        if "total score" not in roster_dict[student_id]:
            #print(email["to"])
            msg = '<p>Please see canvas for your exam score and answer choices, if you took exam via canvas quiz.</p>'
            msg += '<p>If you took an in-person exam, do not worry that you are seeing this message. It is likely that we missed retrieving your scantron - please email both Meena and Andy..</p>'
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


def update_canvas_score(exam_name):
    canvas_data = process_csv("canvas.csv")
    header = canvas_data[0]
    canvas_data = canvas_data[1:]
    for row in canvas_data:
        if row[header.index("Exam 1: HonorLock (1374208)")] != "N/A":
            row[header.index("Exam1 (1379056)")] = row[header.index("Exam 1: HonorLock (1374208)")]
        else:
            net_id = row[header.index("SIS Login ID")].lower()
            net_id = net_id.replace("@wisc.edu", "")
            if net_id in netid_roster_dict:
                if "total score" in netid_roster_dict[net_id]:
                    row[header.index("Exam1 (1379056)")] = netid_roster_dict[net_id]["total score"]
                else:
                    row[header.index("Exam1 (1379056)")] = 0
            else:
                row[header.index("Exam1 (1379056)")] = 0

    canvas_data.insert(0, header)

    with open("canvas_" + exam_name + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(canvas_data)

def main():
    if len(sys.argv) < 4:
        print('Usage: python {} <exam_roster.csv> <exam_results.csv> <exam name, for ex: exam1>'.format(sys.argv[0]))
        sys.exit(1)

    exam_roster = process_csv(sys.argv[1])
    read_roster(exam_roster)

    exam_results = process_csv(sys.argv[2])
    read_exam_results(exam_results)

    exam_name = sys.argv[3]
    gen_email(exam_name)

    convert_roster_to_netid_roster()

    update_canvas_score(exam_name)

if __name__ == '__main__':
    main()
