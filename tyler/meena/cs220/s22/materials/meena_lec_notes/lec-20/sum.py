# STEP 1: Copy and paste code for reading JSON file.

import json
import sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc


# STEP 2: Create a new "numsA.json".
#         Add the list [1, 2, 3, 4] to "numsA.json" file.
#         Use jupyter notebook to create and edit the new file

# STEP 3: Process numsA.json as a command line argument using sys module.
inputFile = sys.argv[1]

# STEP 4: Read the JSON file passed as first command line argument.
data = read_json(inputFile)

# STEP 5: Print type of data returned by function that reads JSON file.

print(type(data))

# STEP 6: Using Python built-in function sum(...), calculate total of numbers in numsA.json.
print(sum(data))

# STEP 7: Create a new JSON file "numsB.json" and try out the following data:
#         [-1, 10, 4,]
#         Does that work?
#         Change the data to [-1, 10, 4] and try to run the program by passing numsB.json

# STEP 8: Create a new JSON file "simple.json" and try out the following data.
#         What kind of error do you get with this?
#         Fix the error by commenting the line of code!
#         3.14
#         True
#         true
#         'hello'
#         "hello"
