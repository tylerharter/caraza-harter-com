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
if len(sys.argv) != 3:
    print("Usage: python3 nearest.py X Y")
    sys.exit()
    
start_x = float(sys.argv[1])
start_y = float(sys.argv[2])
print(start_x, start_y)

data = process_csv("restaurants.csv")

best_distance = None
best_name = None

for :
    # OK to hardcode indexes, since there is
    # no header (no other choice!!!)
    name = row[0]
    x = float(row[1])
    y = float(row[2])
    d = ((x-start_x)**2 + (y-start_y)**2) ** 0.5
    if best_name == None or d < best_distance:
        best_name = name
        best_distance = d

print(f"restaurant {best_name} is only {best_distance} units away")
    
