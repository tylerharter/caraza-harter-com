#!/bin/env python3

import os, sys, random, json

TA = {}
TA["old"] = []
with open("tas.json") as f:
    TA["new"] = [row["name"] for row in json.load(f)]
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
