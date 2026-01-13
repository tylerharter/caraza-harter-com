import os, sys, json, re, subprocess

def main():
    if os.path.exists("renumber.txt"):
        with open("renumber.txt") as f:
            dirs = f.read().strip().splitlines()
            new_dirs = [f"{i+1:02d}{orig[2:]}" for i, orig in enumerate(dirs)]
            for orig_name, new_name in zip(dirs, new_dirs):
                if orig_name == new_name:
                    continue
                cmd = ["git", "mv", os.path.join("lec", orig_name), os.path.join("lec", new_name)]
                print(" ".join(cmd))
                print(str(subprocess.check_output(cmd), "utf-8"))
        os.remove("renumber.txt")

    else:
        dirs = sorted([d for d in os.listdir("lec") if re.match(r"\d\d\-.*", d)])
        with open("renumber.txt", "w") as f:
            f.write("\n".join(dirs) + "\n")
        print("Modify renumber.txt, then run again")

if __name__ == '__main__':
     main()
