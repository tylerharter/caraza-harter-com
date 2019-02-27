import sys, csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename, encoding="utf-8")
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

def dist(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

x = float(sys.argv[1])
y = float(sys.argv[2])

rows = process_csv("restaurants.csv")
best_row = None
best_distance = None
for row in rows:
    d = dist(x, y, float(row[1]), float(row[2]))
    if best_row == None or d <= best_distance:
        best_distance = d
        best_row = row

print(best_row[0])
















        
