import os, sys, json

def main():
    exclude = ["<b>Watch</b>", "QUIZ", "Lab:"]

    for d, _, files in os.walk("lec"):
        for name in files:
            if name != "meta.txt":
                continue
            path = os.path.join(d, name)
            print(path)

            lines = []
            with open(path) as f:
                for line in f:
                    for ex in exclude:
                        if ex in line:
                            break
                    else:
                        lines.append(line)
            out = "".join(lines)
            out = out.replace("f21", "s22").replace("\n\n", "\n")
            with open(path, "w") as f:
                f.write(out)
            print(path)

if __name__ == '__main__':
     main()
