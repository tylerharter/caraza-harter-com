#!/usr/local/bin/python3

import os, sys, json, re
from subprocess import check_output
from bs4 import BeautifulSoup
import requests

with open("canvas-course.txt") as f:
    course_id = int(f.read())

with open("canvas.cred") as f:
    cred = f.read().strip()
    
def cget(url):
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print(url)
    r = requests.get(url, headers={"Authorization": "Bearer "+cred})
    r.raise_for_status()
    return r.json()

def cpost(url, data={}):
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("POST", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("HERE", r.text)
    r.raise_for_status()
    return r.json()

def cput(url, data):
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("PUT", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.put(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()
    return r.json()

def cdelete(url):
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("DELETE", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.delete(url, headers=headers)
    r.raise_for_status()
    return r.json()

def main():
    pages = {p["title"]: p for p in cget("pages")}

    for root, _, fnames in sorted(list(os.walk("."))):
        for fname in fnames:
            if fname == "meta.txt":
                path = os.path.join(root, fname)
                with open(path) as f:
                    title = f.readline().lstrip("#").strip()
                    other = f.read()
                with open("tmp.txt", "w") as f:
                    f.write("### Topics\n\n" + other)
                html = str(check_output(["pandoc", "tmp.txt"]), "utf-8")
                if title in pages:
                    print("DELETE")
                    url = pages[title]["url"]
                    cdelete(f"pages/{url}")
                print("NEW")
                r = cpost("pages",
                          {"wiki_page": {"title": title, "body": html}})

if __name__ == '__main__':
     main()
