import csv, sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
  exampleFile = open(filename)
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

def dist(x1, y1, x2, y2):
    return ((x1-x2) ** 2 + (y1-y2) ** 2) ** 0.5

# grab input data
rows = process_csv("restaurants.csv")
COL_NAME = 0
COL_X = 1
COL_Y = 2

for row in rows:
    row[COL_X] = float(row[COL_X])
    row[COL_Y] = float(row[COL_Y])

# grab user location
user_x = float(sys.argv[1])
user_y = float(sys.argv[2])

best = rows[0]

for row in rows:
    dist_to_row = dist(row[COL_X], row[COL_Y], user_x, user_y)
    dist_to_best = dist(best[COL_X], best[COL_Y], user_x, user_y)
    if dist_to_row < dist_to_best:
        best = row

print(best[COL_NAME])






