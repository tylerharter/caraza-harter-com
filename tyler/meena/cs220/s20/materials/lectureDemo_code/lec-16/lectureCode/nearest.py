import csv
import sys

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

rows = process_csv("restaurants.csv")

def distance(x1, x2, y1, y2):
    #Distance between two points on a plane
    # ((x1 - x2) ^ 2 + (y1 - y2) ^ 2 ) ^ 0.5
    x = (x1 - x2) ** 2
    y = (y1 - y2) ** 2
    distance = (x + y) ** 0.5
    return distance

coord = sys.argv[1]
human_x, human_y = coord.split(",")
human_x = int(human_x)
human_y = int(human_y)

bestRestIndex = 0
bestDistance = distance(human_x, int(rows[0][1]), human_y, int(rows[0][2]))

for index in range(len(rows)):
    currDistance = distance(human_x, int(rows[index][1]), human_y, int(rows[index][1]))
    if currDistance < bestDistance:
        bestRestIndex = index
        bestDistance = currDistance

print(rows[bestRestIndex][0])
