import csv

# copied from https://automatetheboringstuff.com/chapter14/
def process_csv(filename):
    exampleFile = open(filename)
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData

def main():
    rows = process_csv('tornados.csv')
    # rows = rows[:5] # TODO: remove me later

    header = rows[0]
    rows = rows[1:]
    year_idx = header.index("year")

    # key: year
    # val: how many were there in that year
    counts = {}

    for tornado in rows:
        year = tornado[year_idx]
        if year in counts:
            counts[year] = counts[year] + 1
        else:
            counts[year] = 1

    print(counts)


if __name__ == '__main__':
    main()
