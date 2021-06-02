#!/usr/local/bin/python3

import os, sys, json
import requests
from subprocess import check_output
from bs4 import BeautifulSoup

course_id = 222429
existing_videos = {}

def cget(url):
    with open("canvas.cred") as f:
        cred = f.read().strip()
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print(url)
    r = requests.get(url, headers={"Authorization": "Bearer "+cred})
    r.raise_for_status()
    return r.json()

def cpost(url, data={}):
    with open("canvas.cred") as f:
        cred = f.read().strip()
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("POST", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()
    return r.json()

def cput(url, data):
    with open("canvas.cred") as f:
        cred = f.read().strip()
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("PUT", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.put(url, headers=headers, data=json.dumps(data))
    r.raise_for_status()
    return r.json()

def cdelete(url):
    with open("canvas.cred") as f:
        cred = f.read().strip()
    url = f"https://canvas.wisc.edu/api/v1/courses/{course_id}/{url}"
    print("DELETE", url)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer "+cred}
    r = requests.delete(url, headers=headers)
    r.raise_for_status()
    return r.json()

def main():
    r = cget("modules?per_page=500")
    for row in r:
        r = cdelete(f"modules/{row['id']}")

if __name__ == '__main__':
     main()
