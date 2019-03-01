import sys
import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

print(sys.argv)
print(type(sys.argv))

filename = sys.argv[1]
column = sys.argv[-1]
# have column and filename, based on user's desires
rows = process_csv(filename)
header = rows[0]
rows = rows[1:]
# TODO: remove this later
rows = rows[:5] # for debugging, test with just 5 rows

idx = header.index(column)
print("HEADER", header)
print("column", column, "is at", idx)

for row in rows:
    print(row[0], row[idx])
