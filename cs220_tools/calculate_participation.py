import csv
import os
import sys

################################################################################
# 1. Create piazza_list by going to Manage Enrollment "Download Roster as CSV".
#    (just copy paste email column and delete the header)
# 2. Create who_are_you_list by going to Who are you survey results and copying
#    just the email column (delete header)
# 3. Download canvas grades csv file and save it as "canvas.csv" in local dir
# 4. Sample script execution:
#    python3 calculate_participation.py piazza.csv survey.csv "Piazza sign-up (1351636)" "CS220 Student Information Survey (1350484)"
################################################################################

def process_csv(filename):
	fh = open(filename)
	reader = csv.reader(fh)
	data = list(reader)
	return data

def write_csv(filename, data):
	with open(filename, "w") as FH:
		writer = csv.writer(FH)
		writer.writerows(data) 

def read_emails(inFile):
    emails = {}
    with open(inFile, "r") as FH:
        for line in FH:
            line = line.strip()
            emails[line.lower()] = 1
    return emails

def merge_emails(piazza_dict, who_are_you_dict):
    for email in who_are_you_dict:
        if email not in piazza_dict:
            piazza_dict[email] = 1
    return piazza_dict

def update_participation(grade_data, piazza_emails, survey_emails, piazza_column, survey_column):
    header = grade_data[0]
    count = 0
    piazza_index = header.index(piazza_column)
    survey_index = header.index(survey_column)
    email_index = header.index("SIS Login ID")
    
    for (index, row) in enumerate(grade_data):
        if index < 3 or index == len(grade_data) - 1:
            #Skip header rows and test student row
            continue
        if row[email_index].lower() in piazza_emails:
            grade_data[index][piazza_index] = 1
        else:
            grade_data[index][piazza_index] = 0

        if row[email_index].lower() in survey_emails:
            grade_data[index][survey_index] = 1
        else:
            grade_data[index][survey_index] = 0

    return grade_data

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 {} <piazza.csv> <survey.csv> <canvas Piazza column ex: Piazza sign-up (1351636)> <canvas survey column ex: CS220 Student Information Survey (1350484)>".format(sys.argv[0]))
        sys.exit(0)

    piazza_emails = read_emails(sys.argv[1])
    survey_emails = read_emails(sys.argv[2])
    # Old processing
    # merged_emails = merge_emails(piazza_emails, who_are_you_emails)

    grade_data = process_csv("canvas.csv")

    piazza_column = sys.argv[3]
    survey_column = sys.argv[4]

    grade_data = update_participation(grade_data, piazza_emails, survey_emails, piazza_column, survey_column)
    write_csv("canvas_participation.csv", grade_data)

if __name__ == "__main__":
    main()
