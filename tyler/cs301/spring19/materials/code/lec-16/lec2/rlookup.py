import sys, csv

print(sys.argv)

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

target = sys.argv[1]
print(target)

rows = process_csv("restaurants.csv")
found_row = None
for row in rows:
    if row[0] == target:
        found_row = row

if found_row != None:
    print("location x={}, y={}".format(found_row[1],
                                       found_row[2]))
else:
    print("not found")
