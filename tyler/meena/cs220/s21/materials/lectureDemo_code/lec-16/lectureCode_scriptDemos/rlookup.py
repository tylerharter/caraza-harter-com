import csv
import sys

# copied from https://automatetheboringstuff.com/2e/chapter16/ 
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

#Check out argument list from sys
#print("ARGV", sys.argv)
search = sys.argv[1]

rows = process_csv("restaurants.csv")
for row in rows:
    if row[0].lower() == search.lower():
        print("x={}, y={}".format(row[1], row[2]))
