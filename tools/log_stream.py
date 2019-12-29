import os, sys, gzip, json

def event_iter():
    for root, _, files in os.walk("snapshot/logs/kinesis2019/12"):
        for name in files:
            path = os.path.join(root, name)
            with gzip.GzipFile(path) as f:
                for l in f:
                    yield json.loads(l)

def main():
    for event in event_iter():
        print(event['request'].keys())

if __name__ == '__main__':
    main()
