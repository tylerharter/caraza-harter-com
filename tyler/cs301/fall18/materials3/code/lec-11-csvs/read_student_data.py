import csv


# Copied from http://automatetheboringstuff.com/chapter14/
exampleFile = open('student_data.csv')
exampleReader = csv.reader(exampleFile)
header = next(exampleReader)
exampleData = list(exampleReader)
# print(exampleData)

for row in exampleData:
    print(row)

# print(header)

total = 0
for student in exampleData:
    total += float(student[3])

print('total =', total)

num_students = len(exampleData)
print('num students =', num_students)

print('average =', round(total/num_students, 2))

# print students whose last name starts with K
for student in exampleData:
    if student[0].startswith('K'):
        print(student[0])