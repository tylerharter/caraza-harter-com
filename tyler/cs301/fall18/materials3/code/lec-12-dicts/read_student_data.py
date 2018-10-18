import csv

# Copied from http://automatetheboringstuff.com/chapter14/
exampleFile = open('student_data.csv')
exampleReader = csv.reader(exampleFile)
exampleData = list(exampleReader)
# print(exampleData)

print('exampleData: ', exampleData)

header = exampleData[0]
data = exampleData[1:]

for row in data:
    print(row)

print('header:', header)

# print email addresses
print('index = ', header.index('Email Address'))
emails = []
for stud in data:
    # print(stud[header.index('Email Address')])
    emails.append(stud[header.index('Email Address')])

print(emails)

netids = []
for email in emails:
    netids.append(email.split('@')[0])

print(netids)

fullnames = []
for student in data:
    fullname = student[header.index('First Name')] + " " + student[header.index('Last Name')]
    fullnames.append(fullname)

print(fullnames)
