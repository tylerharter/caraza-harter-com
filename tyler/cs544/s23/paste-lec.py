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
        if num in lookup:
            pass
        else:
            short = title.split()[0].lower()
            dirname = f"lec/{num}-{short}"
            os.mkdir(dirname)
            with open(f"{dirname}/meta.txt", "w") as f:
                f.write(title + "\n")
    print(matches)

if __name__ == '__main__':
     main()
