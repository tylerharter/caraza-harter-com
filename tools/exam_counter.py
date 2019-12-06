import os, sys, json

def main():
    for exam in ["exam1", "exam2", "final"]:
        print("="*40)
        print(exam)
        print("="*40)
        counts = {}
        with open("roster.json") as f:
            for row in json.load(f):
                place = row.get(exam)
                counts[place] = counts.get(place, 0) + 1
        print(json.dumps(counts, indent=2))

if __name__ == '__main__':
     main()
