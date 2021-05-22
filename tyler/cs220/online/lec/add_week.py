import os, sys, json, requests
from subprocess import check_output
import pandas as pd

course_id = 244425

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
    print("HERE", r.text)
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

class Module:
    def __init__(self, name):
        r = cpost("modules", {"module": {"name": name}})
        self.mod_id = r["id"]

    def add_page(self, name, content):
        r = cpost("pages",
                  {"wiki_page": {"title": name,
                                 "body": content}})
        page_url = r["url"]

        r = cpost(f"modules/{self.mod_id}/items",
                  {"module_item": {"title": name,
                                   "type": "Page",
                                   "page_url": page_url,
                                   "completion_requirement": {"type": "must_mark_done"}}})        

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 add_week.py <week-num> <dir1> <dir2> <dir3>")
        return
    week = int(sys.argv[1])
    days = sys.argv[2:5]

    m = Module(f"Week {week}")
    for i, day in enumerate(days):
        dnum = i+1

        url = f"https://github.com/tylerharter/caraza-harter-com/tree/master/tyler/cs320/s21/lec/{day}"
        m.add_page(f'Watch (W{week}.{dnum})', f'<p>Watch this: <a href="{url}">{url}</a></p><br>')

        if os.path.exists(os.path.join("lec", day, "reading.html")):
            url = f"https://tyler.caraza-harter.com/cs320/s21/lec/{day}/reading.html"
            m.add_page(f'Read (W{week}.{dnum})', f'<p>Read this: <a href="{url}">{url}</a></p><br>')

        if dnum == 1:
            url = f"https://github.com/tylerharter/cs320/tree/master/s21/lab{week}"
            m.add_page(f'Lab (W{week})', f'<p>Do this: <a href="{url}">{url}</a></p><br>')

if __name__ == '__main__':
     main()
