import os, sys, json

def main():
    counts = {}
    with open("roster.json") as f:
        for row in json.load(f):
            exam = row.get("final")
            counts[exam] = counts.get(exam, 0) + 1
    print(json.dumps(counts, indent=2))

if __name__ == '__main__':
     main()
