import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

if len(sys.argv) != 3:
    print("Usage: python dump.py <data.csv> <col>")
    sys.exit()

rows = process_csv(sys.argv[1])

# split header apart from data
header = rows[0]
rows = rows[1:]
target = sys.argv[2]
print(header)
print("we are searching for", target)
position = header.index(target)
print("that column is at index", position)

for row in rows:
    print(row[0], row[position])
