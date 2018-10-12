import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename)
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData

rows = process_csv("restaurants.csv")
target = "subway"
for row in rows:
    if row[0].lower() == target.lower():
        print("X={}, Y={}".format(row[1], row[2]))
