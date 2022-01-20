import os, sys, json

def lines(path):
    with open(path) as f:
        return [l.strip() for l in f]

def main():
    assert sys.argv[1] in ("read", "write")
    if sys.argv[1] == "read":
        paths = []
        for root, _, names in os.walk("lec"):
            for name in names:
                if name == "meta.txt":
                    paths.append(os.path.join(root, name))
        paths.sort()
        metas = [{"path": p, "lines": lines(p)} for p in paths]
        with open("metas.json", "w") as f:
            json.dump(metas, f, indent=2)
    else:
        with open("metas.json") as f:
            metas = json.load(f)
        for meta in metas:
            with open(meta["path"], "w") as f:
                f.write("\n".join(meta["lines"]) + "\n")

if __name__ == '__main__':
     main()
