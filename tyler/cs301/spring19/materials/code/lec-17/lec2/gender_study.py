import sys
import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

# STEP 1: classify names
fnames = []
mnames = []

rows = process_csv("names.csv")
for row in rows[1:]:
    if row[1] == "boy":
        mnames.append(row[0])
    elif row[1] == "girl":
        fnames.append(row[0])

print("Female", fnames[:5])
print("Male", mnames[:5])

# STEP 2: count deaths
rows = process_csv("hurricanes.csv")
header = rows[0]

mdeaths = []
fdeaths = []

for row in rows[1:]:
    name = row[header.index("name")]
    deaths = int(row[header.index("deaths")])
    if name in fnames and not name in mnames:
        fdeaths.append(deaths)
    elif name in mnames and not name in fnames:
        mdeaths.append(deaths)

print("Female Avg:", sum(fdeaths) / len(fdeaths))
print("Male Avg:", sum(mdeaths) / len(mdeaths))







