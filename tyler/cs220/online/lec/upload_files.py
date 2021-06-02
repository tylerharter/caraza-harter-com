import os, sys, json, requests, re
from subprocess import check_output

def canvas_upload(dirname, filename, canvas_dir):
    with open("canvas.cred") as f:
        cred = f.read().strip()
    r = requests.post("https://canvas.wisc.edu/api/v1/courses/222429/files",
                      data={"name": filename,
                            "parent_folder_path": canvas_dir},
                      headers={"Authorization": "Bearer "+cred})
    r.raise_for_status()

    r = r.json()
    url = r["upload_url"]
    upload = r["upload_params"]
    with open(os.path.join(dirname, filename), "rb") as f:
        r = requests.post(url, data=upload, files={"file": f})
    r.raise_for_status()

def should_skip(path):
    parts = path.split(os.path.sep)
    if len(parts) == 1:
        return True
    dirname, fname = os.path.sep.join(parts[:-1]), parts[-1]
    if fname in ["meta.txt", "notes.txt"]:
        return True
    if fname == "pytutor.html":
        return False
    if "worksheet-long" in fname:
        return True
    if fname.endswith(".html") or fname.endswith(".md") or fname.endswith(".pages") or fname.endswith(".key"):
        return True
    return False
    
def main():
    paths = str(check_output("git ls-tree -r master --name-only", shell=True), "utf-8")
    paths = [p for p in paths.split("\n") if not should_skip(p)]
    for i, path in enumerate(paths):
        print(f"{i+1} of {len(paths)}: {path}")
        parts = path.split(os.path.sep)
        dirname, fname = os.path.sep.join(parts[:-1]), parts[-1]
        canvas_upload(dirname, fname, "lessons/"+dirname)
        break

if __name__ == '__main__':
     main()
