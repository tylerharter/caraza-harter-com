import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

# part 1: classify names
rows = process_csv("names.csv")
rows[1:]
boy_names = []
girl_names = []
for row in rows:
    if row[1] == "boy":
        boy_names.append(row[0])
    elif row[1] == "girl":
        girl_names.append(row[0])
print("girl names:", girl_names[:5])
print("boy names:", boy_names[:5])

# part 2: count deaths of hurricanes, by name gender
rows = process_csv("hurricanes.csv")
header = rows[0]
rows = rows[1:]

# list of all deaths
female_hur = []
male_hur = []

for row in rows:
    name = row[header.index("name")]
    deaths = int(row[header.index("deaths")])
    if name in girl_names and not name in boy_names:
        female_hur.append(deaths)
    elif name in boy_names and not name in girl_names:
        male_hur.append(deaths)
print("f avg", sum(female_hur) / len(female_hur))
print("m avg", sum(male_hur) / len(male_hur))
