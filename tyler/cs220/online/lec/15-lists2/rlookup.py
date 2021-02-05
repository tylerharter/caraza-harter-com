import csv
import sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

print(sys.argv)
if len(sys.argv) < 2:
    print("WARNING!  No restaurant.")
    sys.exit()
    
print("Find:", sys.argv[1])
target = sys.argv[1]

data = process_csv("restaurants.csv")
for row in data:
    # OK to hardcode indexes, since there is
    # no header (no other choice!!!)
    name = row[0]
    x = row[1]
    y = row[2]
    if name.lower() == target.lower():
        print(f"x={x}, y={y}")
