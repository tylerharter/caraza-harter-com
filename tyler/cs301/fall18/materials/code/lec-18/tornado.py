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
    # val: list of tornados in that year
    buckets = {}

    for tornado in rows:
        year = tornado[year_idx]
        if year in buckets:
            buckets[year].append(tornado)
        else:
            buckets[year] = [tornado]

    for year in buckets:
        tornados = buckets[year]
        print(year, median(tornados))

def median(bucket):
    speeds = []
    for row in bucket:
        speeds.append(int(row[-1]))
    speeds.sort()
    if len(speeds) % 2 == 1:
        return speeds[len(speeds) // 2]
    else:
        return (speeds[len(speeds) // 2 - 1] + speeds[len(speeds) // 2]) / 2

if __name__ == '__main__':
    main()
