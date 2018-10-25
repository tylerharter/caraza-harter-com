# copied from https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file

import json
from pprint import pprint

with open('/Users/gerald/PycharmProjects/CS301/Lecture14-TuplesAndObjects/person.json') as f:
    data = json.load(f)

pprint(data)




