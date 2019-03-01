import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

rows = process_csv("hurricanes.csv")

# split header apart from data
header = rows[0]
rows = rows[1:]

# index: what year it is
# value: how many hurricanes were in that year
year_counts = [0] * 2100

for row in rows:
    year = int(row[header.index("year")])
    year_counts[year] += 1

for year in range(len(year_counts)):
    count = year_counts[year]
    if count > 0:
        print(year, count)
