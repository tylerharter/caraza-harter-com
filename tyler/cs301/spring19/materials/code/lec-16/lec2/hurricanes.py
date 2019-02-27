import sys, csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

rows = process_csv("h10.csv")
header = rows[0]
data = rows[1:]

print(header)

for row in data:
    print(row[header.index("deaths")])
