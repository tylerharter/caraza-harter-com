import os, sys, csv, json

def main():
    states = []
    with open('population.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row.pop('State').replace(' ', '_') + '.json'
            states.append(path)
            for k in row:
                row[k] = int(row[k])
            with open(path, 'w') as out:
                json.dump(row, out)
    with open('state_files.txt', 'w') as f:
        f.write('\n'.join(states))

if __name__ == '__main__':
    main()
