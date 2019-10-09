import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

search = sys.argv[1]
print("SEARCH FOR", search)

rows = process_csv("restaurants.csv")
for row in rows:
    if search == row[0]:
        print("x =", row[1], " AND y =", row[2])
