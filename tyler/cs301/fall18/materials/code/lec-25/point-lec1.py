import json, sys

def main():
    path = 'points.json'

    # read raw
    try:
        f = open(path)
        data = f.read()
        f.close()
    except:
        data = '{}'

    # raw to structures
    jdata = json.loads(data)
    print("JSON PARSED:", jdata)

    # give a point
    name = sys.argv[1]
    if name in jdata:
        jdata[name] += 1
    else:
        jdata[name] = 1
    print(jdata)

    # write file
    raw = json.dumps(jdata)
    fout = open(path, "w")
    fout.write(raw)
    fout.close()

main()