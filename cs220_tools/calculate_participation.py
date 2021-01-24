import csv
import os
import sys

################################################################################
# 1. Create piazza_list by going to Manage Enrollment "Download Roster as CSV".
#    (just copy paste email column and delete the header)
# 2. Create who_are_you_list by going to Who are you survey results and copying
#    just the email column (delete header)
# 3. Download canvas grades csv file and save it as "canvas.csv" in local dir
# 4. Run this script: python3 calculate_participation.py "Participation (1031490)"
#    (argument is participation column name from cavas.csv)
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

def readEmails(inFile):
    emails = {}
    with open(inFile, "r") as FH:
        for line in FH:
            line = line.strip()
            emails[line.lower()] = 1
    return emails

def mergeEmails(piazza_dict, who_are_you_dict):
    for email in who_are_you_dict:
        if email not in piazza_dict:
            piazza_dict[email] = 1
    return piazza_dict

def update_participation(grade_data, merged_emails):
    header = grade_data[0]
    count = 0
    participation_index = header.index(sys.argv[1])
    email_index = header.index("SIS Login ID")
    for (index, row) in enumerate(grade_data):
        if index < 3 or index == len(grade_data) - 1:
            #Skip header rows and test student row
            continue
        if row[email_index].lower() in merged_emails:
            grade_data[index][participation_index] = 1
        else:
            grade_data[index][participation_index] = 0
    return grade_data

def main():
    piazza_emails = readEmails("piazza_list")
    who_are_you_emails = readEmails("who_are_you_list")
    merged_emails = mergeEmails(piazza_emails, who_are_you_emails)

    grade_data = process_csv("canvas.csv")
    grade_data = update_participation(grade_data, merged_emails)
    write_csv("canvas_participation.csv", grade_data)

if __name__ == "__main__":
    main()
