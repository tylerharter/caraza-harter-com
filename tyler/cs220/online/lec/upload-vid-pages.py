#!/usr/local/bin/python3

import os, sys, json
import requests
from subprocess import check_output
from bs4 import BeautifulSoup

course_id = 222429
#course_id = 254527 # Peyman
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

def add_discussion(name, content):
    r = cpost("discussion_topics",
              {"title": name,
               "message": content,
               "discussion_type": "threaded"})

def update_discussion(discussion_id, content):
    r = cput(f"discussion_topics/{discussion_id}",
             {"message": content})

def main():
    r = cget("discussion_topics?per_page=500")
    existing_videos.update({row["title"]: row["id"] for row in r})
    print("EXISTING:", ", ".join(sorted(existing_videos.keys())))

    videos = []
    for root, _, fnames in os.walk("."):
        videos.extend([os.path.join(root, fname) for fname in fnames
                       if fname.endswith(".mp4")])

    videos.sort(reverse=True)
    for vid in videos:
        if len(sys.argv) == 1:
            upload_video_doc(vid)
        for filter_text in sys.argv[1:]:
            if filter_text in vid:
                upload_video_doc(vid)
                break

def upload_video_doc(mp4_path):
    html_path = mp4_path.replace(".mp4", ".html")

    with open(html_path) as f:
        name = mp4_path.replace("./", "cs220/")
        html = f.read()
        if name in existing_videos:
            print("UPDATE", name)
            update_discussion(existing_videos[name], html)
        else:
            print("ADD", name)
            add_discussion(name, html)

if __name__ == '__main__':
     main()
