import os, sys, json, re
from shutil import copyfile
from subprocess import check_output

def main():
    with open('schedule.bak') as f:
        days = f.read().split('=\n')[1:]
    for i, day in enumerate(days):
        num = i+1
        lines = day.split("\n")
        name = f"{num:02d}-{lines[0]}"
        dirname = os.path.join("lec", name)
        os.makedirs(dirname)

        for i in range(len(lines)):
            line = lines[i]
            for m in re.findall(r'\"((materials|lectures|reading).*?)\"', line):
                path1 = m[0]
                name = path1.split("/")[-1]
                if re.match("lec-\d\d.pdf", name):
                    name = "slides.pdf"
                path2 = os.path.join(dirname, name)
                print(path1, path2)
                copyfile(path1, path2)
                assert(path1 in line)
                lines[i] = lines[i].replace(path1, path2)
                if path1.endswith(".pdf"):
                    path1 = path1.replace(".pdf", ".key")
                    path2 = path2.replace(".pdf", ".key")
                    if os.path.exists(path1):
                        print(path1, path2)
                        copyfile(path1, path2)
                        lines[i] = line.replace(path1, path2)

        for i in range(len(lines)):
            if "SLIDES" in lines[i]:
                lines[i] = "SLIDES"
        day = "\n".join(lines[1:])
        with open(os.path.join(dirname, "meta.txt"), "w") as f:
            f.write(day)

if __name__ == '__main__':
     main()
