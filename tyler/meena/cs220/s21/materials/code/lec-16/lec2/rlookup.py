import csv
import sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

print("ARGV", sys.argv)
search = sys.argv[1]

rows = process_csv("restaurants.csv")
for row in rows:
    if row[0] == search:
        print("X={}, Y={}".format(row[1], row[2]))
