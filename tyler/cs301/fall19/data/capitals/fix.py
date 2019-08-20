import os, sys, json

def main():
    for path in os.listdir("."):
        if path.endswith(".json"):
            with open(path) as f:
                data = json.load(f)
            with open(path, "w") as f:
                json.dump(data, f, indent=2, sort_keys=True)
                
if __name__ == '__main__':
     main()
