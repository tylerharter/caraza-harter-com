import csv
import os
import sys

################################################################################
# 1. Create who_are_you_list by going to Who are you survey results and copying
#    just the email column (delete header)
# 2. Download canvas grades csv file and save it as "canvas.csv" in local dir
# 3. Sample script execution:
#    python3 calculate_participation_information_survey.py survey.csv "CS220 Student Information Survey (1350484)"
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

def update_participation(grade_data, survey_emails, survey_column):
    header = grade_data[0]
    count = 0
    survey_index = header.index(survey_column)
    email_index = header.index("SIS Login ID")
    
    for (index, row) in enumerate(grade_data):
        if index < 3 or index == len(grade_data) - 1:
            #Skip header rows and test student row
            continue

        if row[email_index].lower() in survey_emails:
            grade_data[index][survey_index] = 1
        else:
            grade_data[index][survey_index] = 0

    return grade_data

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 {} <survey.csv> <canvas survey column ex: CS220 Student Information Survey (1350484)>".format(sys.argv[0]))
        sys.exit(0)

    survey_emails = read_emails(sys.argv[1])
    grade_data = process_csv("canvas.csv")

    survey_column = sys.argv[2]

    grade_data = update_participation(grade_data, survey_emails, survey_column)
    write_csv("canvas_participation.csv", grade_data)

if __name__ == "__main__":
    main()
