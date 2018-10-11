import csv

def process_csv(filename):
  exampleFile = open(filename)
  exampleReader = csv.reader(exampleFile)
  exampleData = list(exampleReader)
  return exampleData

def main():
    rows = process_csv('hurricanes_short.csv')
    print(rows)

main()