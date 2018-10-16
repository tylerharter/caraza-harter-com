import csv

studentsFile = open('students.csv')
studentsReader = csv.reader(studentsFile)
header = next(studentsReader)
studentsData = list(studentsReader)

# print('header =', header)
# print(studentsData)

# for student in studentsData:
#     print(student)

# number of students in the class
print('number of students in the class =', len(studentsData))

# extract the netids and store it in a list
# netids = []
# for student in studentsData:
#     email = student[header.index('Email Address')]
#     email_parts = email.split("@")
#     netid = email_parts[0]
#     netids.append(netid)
# print(netids)

# print student names starting with A
# for student in studentsData:
#     if student[header.index('Name')].startswith('A'):
#         print(student)

total = 0
for stud in studentsData:
    total += int(stud[header.index('Score')])
mean = round(total / len(studentsData), 2)
print('mean score =', mean)

