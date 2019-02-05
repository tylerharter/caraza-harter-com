import os, sys, random

TA = {}
TA["old"] = ["Bob", "Mitali", "Om", "Shruthi", "Ushmal"]
TA["new"] = ["Ashay", "Chakshu", "Deepan", "Hugh", "Zhanpeng"]
TA["all"] = TA["old"] + TA["new"]

def main():
    category = sys.argv[1]
    times = int(sys.argv[2])
    tas = []
    for i in range(times):
        random.shuffle(TA[category])
        tas += TA[category]
    print("\n".join(tas))

if __name__ == '__main__':
    main()
