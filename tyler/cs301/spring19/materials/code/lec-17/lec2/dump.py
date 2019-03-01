import sys
import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

filename = sys.argv[1]
column = sys.argv[2]

print(filename, column)
rows = process_csv(filename)
header = rows[0]
rows = rows[1:]

print("HEADER", header)
idx = header.index(column)
print(column, "is at index", idx)

for row in rows:
    print(row[0], row[idx])

















    
