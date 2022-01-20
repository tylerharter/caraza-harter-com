import os, sys, json
import shutil
from subprocess import check_output

def main():
    if sys.argv[1] == "insert":
        num = int(sys.argv[2])
        for name in sorted(os.listdir("lec"), reverse=True):
            parts = name.split("-")
            if not parts[0].isdigit():
                continue
            if int(parts[0]) < num:
                continue
            parts[0] = "%02d" % (int(parts[0]) + 1)
            name2 = "-".join(parts)
            cmd = ["git", "mv",
                          os.path.join("lec", name),
                          os.path.join("lec", name2)]
            check_output(cmd)
    if sys.argv[1] == "delete":
        num = int(sys.argv[2])
        for name in sorted(os.listdir("lec")):
            parts = name.split("-")
            if not parts[0].isdigit():
                continue
            if int(parts[0]) < num:
                continue
            if int(parts[0]) == num:
                shutil.rmtree(os.path.join("lec", name))
            parts[0] = "%02d" % (int(parts[0]) - 1)
            name2 = "-".join(parts)
            cmd = ["git", "mv",
                          os.path.join("lec", name),
                          os.path.join("lec", name2)]
            print(cmd)
            check_output(cmd)
    else:
        print("not implemented")

if __name__ == '__main__':
     main()
