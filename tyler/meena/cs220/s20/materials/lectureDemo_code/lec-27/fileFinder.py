import os
import sys

searchFileName = sys.argv[1]
searchDirectory = sys.argv[2]

def recursiveDirSearch(searchDirectory, searchFileName):
    for curr in os.listdir(searchDirectory):
        curr = os.path.join(searchDirectory, curr)
        #Check if curr is a directory or a file
        if os.path.isfile(curr):
            #If it is a file, check if that is searchFileName
            if searchFileName in curr:
                f = open(curr)
                contents = f.read()
                f.close()
                return contents
        else:
            contents = recursiveDirSearch(curr, searchFileName)
            if contents != None:
                return contents
    return None

if not os.path.exists(searchDirectory):
    print("Unable to find searchDirectory!")
else:
    contents = recursiveDirSearch(searchDirectory, searchFileName)
    if contents != None:
        print(contents, end = "")

