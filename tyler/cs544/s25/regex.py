import os, sys, json, re
from pathlib import Path

PATTERN = r"https://mediaspace.wisc.edu/media/.*"
REPLACE = r""

def main():
    for dirname, _, names in os.walk("lec"):
        dirname = Path(dirname)
        for name in names:
            if name != "meta.txt":
                continue

            path = dirname / name
            print(path)

            with open(path) as f:
                data = f.read()
            data = re.sub(PATTERN, REPLACE, data)
            with open(path, "w") as f:
                f.write(data)

if __name__ == '__main__':
     main()
