import csv
import sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

def distance(x1, x2, y1, y2):
    #Distance between two points on a plane
    # ((x1 - x2) ^ 2 + (y1 - y2) ^ 2 ) ^ 0.5
    x = (x1 - x2) ** 2
    y = (y1 - y2) ** 2
    distance = (x + y) ** 0.5
    return distance

filename = "restaurants.csv"
rows = process_csv(filename)

coord = sys.argv[1]
human_x, human_y = coord.split(",")
human_x = int(human_x)
human_y = int(human_y)

bestIndex = None
bestDistance = None
for index in range(len(rows)):
    row = rows[index]
    restaurant = row[0]
    x = int(row[1])
    y = int(row[2])

    curr_distance = distance(x, human_x, y, human_y)
    if bestDistance == None or curr_distance < bestDistance:
        bestDistance = curr_distance
        bestIndex = index

#print(bestDistance)
print(rows[bestIndex][0])
