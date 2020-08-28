import csv
import sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

# The Sett is closest
parts = sys.argv[1].split(",")
X = float(parts[0])
Y = float(parts[1])

rows = process_csv("restaurants.csv")

def distance(idx):
    rest_x = float(rows[idx][1])
    rest_y = float(rows[idx][2])
    return ((X - rest_x)**2 + (Y - rest_y)**2) ** 0.5

best_i = 0
for i in range(len(rows)):
    row = rows[i]
    if distance(i) < distance(best_i):
        best_i = i
print(rows[best_i][0])





