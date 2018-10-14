import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename)
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData

def main():
    rows = process_csv('tornados.csv')
    print('There are {} rows'.format(len(rows)))

if __name__ == '__main__':
    main()
