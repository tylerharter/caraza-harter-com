import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename)
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

rows = process_csv("restaurants.csv")

COL_NAME = 0
COL_X = 1
COL_Y = 2

target_row = None

print(sys.argv)
for row in rows:
    if row[COL_NAME] == sys.argv[1]:
        target_row = row

if target_row != None:
    print("found it at X={}, Y={}".format(target_row[COL_X],
                                          target_row[COL_Y]))
else:
    print("not found")
