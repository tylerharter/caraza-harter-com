import os, sys, json, re
from subprocess import check_output

def main():
    lookup = {}
    for name in os.listdir("lec"):
        lookup[name.split("-")[0]] = f"lec/{name}"

    txt = str(check_output("pbpaste"), "utf-8")
    matches = re.findall(r"Lecture (\d+): (.+)", txt)
    for num, title in matches:
        if len(num) == 1:
            num = "0"+num

        short = title.split()[0].lower()

        if num in lookup:
            dirname = lookup[num]
            metaname = f"{dirname}/meta.txt"
            with open(metaname) as f:
                lines = list(f) + [""]
            lines[0] = title
            with open(metaname, "w") as f:
                f.write("\n".join(lines) + "\n")
        else:
            dirname = f"lec/{num}-{short}"
            metaname = f"{dirname}/meta.txt"
            os.mkdir(dirname)
            with open(metaname, "w") as f:
                f.write(title + "\n")
    print(matches)

if __name__ == '__main__':
     main()
