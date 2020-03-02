import os, sys, random, string

# this generates tornados.csv.
# you don't need to understand this code!
def main():
    rows = []
    for year in range(1995, 2018):
        count = random.randint(0, 5)
        for _ in range(count):
            tid = ''.join([random.choice(string.ascii_uppercase) for _ in range(8)])
            location = random.choice(['site A', 'site B', 'site C'])
            speed = random.randint(100, 300)
            rows.append([year, tid, location, speed])
    random.shuffle(rows)
    rows = [['year', 'id', 'location', 'speed']] + rows

    with open('tornados.csv', 'w') as f:
        for row in rows:
            f.write(','.join(map(str, row)) + '\n')

if __name__ == '__main__':
    main()
