import hashlib
import csv

################################################################################
# This program requires the response to "Who are you" survey as a csv file named
# "Who_are_you_responses.csv"
#
# Run simply as python3 anonymize_whoAreYouSurvey.py 
################################################################################

def process_csv(filename):
    exampleFile = open(filename)
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData 
rows = process_csv("Who_are_you_responses.csv")
header = rows[0]
email_index = header.index("Email Address")

#Hash the email field
for index, row in enumerate(rows[1:]):
    email = rows[index][email_index].lower()
    hash_object = hashlib.md5(email.encode())
    rows[index][email_index] = hash_object.hexdigest()


#Write updated csv file
with open("Who_are_you_responses_anonymized.csv", "w+") as wFH:
    writer = csv.writer(wFH)
    writer.writerows(rows)
