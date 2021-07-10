import os, sys, json, requests
from subprocess import check_output
import pandas as pd

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

def get_submissions():
    page = 1
    submissions = []
    while True:
        r = cget(f"quizzes/{quiz_id}/submissions?page={page}")
        sublist = r["quiz_submissions"]
        if len(sublist) == 0:
            return submissions
        submissions.extend(sublist)
        page += 1

def show_user(user_id):
    r = cget(f"modules?student_id={user_id}&include[]=items")
    for week in r:
        print("="*40)
        print(week["name"])
        print("="*40)
        for item in week["items"]:
            print(item["title"], {True: "DONE", False: ""}[item["completion_requirement"]["completed"]])

def add_page(self, name, content):
    r = cpost("pages",
              {"wiki_page": {"title": name,
                             "body": content}})
    page_url = r["url"]

    r = cpost(f"modules/{self.mod_id}/items",
              {"module_item": {"title": name,
                               "type": "Page",
                               "page_url": page_url,
                               "completion_requirement": {"type": "must_view"}}})

def main():
    pages = {p["title"]: p for p in cget("pages?per_page=500")}
    folders = cget("folders?per_page=500")
    folders = {f["full_name"]: f for f in folders}
    all_discussions = []
    pg = 1
    while True:
        tmp = cget(f"discussion_topics?per_page=500&page={pg}")
        if tmp:
            all_discussions.extend(tmp)
        else:
            break
        pg += 1
    all_discussions.sort(key=lambda d: d["title"])

    for dirname in sorted(os.listdir(".")):
        meta = os.path.join(dirname, "meta.txt")
        if not os.path.exists(meta):
            continue
        with open(meta) as f:
            # create module
            modnum = int(dirname.split("/")[-1].split("-")[0])
            if modnum not in (27,):
                continue
            modname = f.readline().lstrip("#").strip()
            page = pages[modname]
            modname = (f"{modnum}. {modname}")
            r = cpost("modules", {"module": {"name": modname}})
            mod_id = r["id"]

            # add meta page to beginning of module
            r = cpost(f"modules/{mod_id}/items",
                      {"module_item": {"title": page["title"],
                                       "type": "Page",
                                       "page_url": page["url"]}})

            # find files for this module
            folder = folders[f"course files/lessons/{dirname}"]
            folder_id = folder["id"]
            r = requests.get(f"https://canvas.wisc.edu/api/v1/folders/{folder_id}/files",
                             headers={"Authorization": "Bearer "+cred})
            r.raise_for_status()
            files = {f["filename"]: f for f in r.json()}

            # add discussions (containing videos) to module
            discussions = [d for d in all_discussions
                           if "/" in d["title"] and d["title"].split("/")[1] == dirname]

            for name in ["worksheet.pdf"]:
                if not name in files:
                    continue
                f = files[name]
                r = cpost(f"modules/{mod_id}/items",
                          {"module_item": {"type": "File",
                                           "content_id": f["id"]}})

            for discussion in discussions:
                r = cpost(f"modules/{mod_id}/items",
                          {"module_item": {"type": "Discussion",
                                           "content_id": discussion["id"],
                                           "completion_requirement": {"type": "must_view"}}})

            for name in ["slides.pdf", "reading.pdf", "pytutor.html"]:
                if not name in files:
                    continue
                f = files[name]
                r = cpost(f"modules/{mod_id}/items",
                          {"module_item": {"type": "File",
                                           "content_id": f["id"]}})


if __name__ == '__main__':
     main()
