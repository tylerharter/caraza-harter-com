# Copyright 2018 Tyler Caraza-Harter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, random, time
import os, json, math, pytz
from datetime import datetime, timedelta, timezone

from lambda_framework import *
from roster import *

BANK = 12
PENALTY = 0.05
PROJ_COUNT = 7
NOT_REVIEWED = {"p7"}

def utc_to_cst(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone('US/Central'))

def extension_path(email, project_id):
    return 'extensions/%s/%s.json' % (to_s3_key_str(project_id), to_s3_key_str(email))

def config_path():
    return 'config.json'

def get_deadlines(): # US/Central time zone. Timezone labeled
    deadlines_txt = copy.copy(s3().read_cached_json('config.json')["deadlines"])
    soft_days = copy.copy(s3().read_cached_json('config.json')["soft_days"])
    hard_days = copy.copy(s3().read_cached_json('config.json')["hard_days"])

    deadlines = {}
    for p, ddl in deadlines_txt.items(): 
        deadline = datetime.strptime(ddl, "%m/%d/%y")
        deadline = deadline.replace(tzinfo=pytz.timezone('US/Central'))
        deadline = deadline + timedelta(days=1)
        deadlines[p] = deadline
    return deadlines, soft_days, hard_days



def get_extensions(project_id, nid):
    email = f"{nid}@{NET_ID_EMAIL_SUFFIX}"
    path = extension_path(email, project_id)
    try:
        response = s3().get_object(Bucket=BUCKET, Key=path)
        row = json.loads(str(response['Body'].read(), 'utf-8'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            row = {'days': 0, 'error': None}
        else:
            raise e

    return row.get("days",0)

def get_grade(project_id, nid, latest_sub_dir, submit_time, sub_late_days, extension, sub_soft_days, remaining_late_days): 
    if latest_sub_dir is None: 
        return {"project": project_id, "net_id": nid, 
            "test_score": 0, 
            "submit_time": None, "late_days": 0, "late_penalty": 0, "remaining_late_days": remaining_late_days, 
            "ta_deduction": 0, "score": 0,
            "comment_count": 0, "ready": False, "code_review_url": None}
    sub = s3().read_json_default(os.path.join(latest_sub_dir, "submission.json"), {})
    test = s3().read_json_default(os.path.join(latest_sub_dir, "test.json"), {})
    cr = s3().read_json_default(os.path.join(latest_sub_dir, "cr.json"), {})
    
    if sub:
        late_penalty = max(sub_late_days - sub_soft_days, 0) * PENALTY

    ready = False
    test_score = 0
    if sub and test and (cr or project_id in NOT_REVIEWED):
        test_score = test.get("score", 0)
        ta_deduction = cr.get("points_deducted", 0)
        comment_count = 0
        for comments in cr.get("highlights", {}).values():
            comment_count += len(comments)
        ready = True
         
    if not ready:
        ta_deduction = 0
        comment_count = 0
        score = 0
    else:
        score = max(test_score - ta_deduction, 0) * (1 - late_penalty)
    
    
    return {"project": project_id, "net_id": nid, 
            "test_score": test_score, 
            "submit_time": submit_time, "extension": extension, 
            "late_days": sub_late_days, "late_penalty": late_penalty, "remaining_late_days": remaining_late_days, 
            "ta_deduction": ta_deduction, "score": score,
            "comment_count": comment_count, "ready": ready}

def extract_grades(nid): 
    email = f"{nid}@{NET_ID_EMAIL_SUFFIX}"
    deadlines, soft_days, hard_days = get_deadlines()

    remaining_late_days = BANK

    grades = []
    
    for i in range(1, PROJ_COUNT + 1): 
        project_id = f"p{i}"
        
        extension_days = get_extensions(project_id, nid)
        
        
        individual_dir = f"projects/{to_s3_key_str(project_id)}/{to_s3_key_str(email)}"
        # return list of ALL submissions for this project
        submissions = []
        for path in s3().s3_all_keys(individual_dir):
            link_name = path.split("/")[-1]
            suffix = '-link.json'
            if link_name.endswith(suffix):
                submissions.append(os.path.join(individual_dir, link_name))

        if not links:  
            grades.append(get_grade(project_id, nid, None, 0, soft_days[project_id], remaining_late_days[nid]))     
            continue     
        
        links = sorted(links, reverse=True)

        latest_sub_dir = None
        links_idx = 0
        while True: 
            submission_dir = s3().read_json(links[links_idx])['symlink']
            sub = s3().read_json_default(os.path.join(submission_dir, "submission.json"), {})
            
            if sub: 
                submitted = datetime.strptime(sub["submit_time_utc"], "%Y-%m-%d %H:%M:%S")
                submitted = utc_to_cst(submitted)
                submit_time = datetime.strftime(submitted, "%Y-%m-%d %H:%M:%S %z")
                sub_late_days = math.ceil((submitted - deadlines[project_id]) / timedelta(days=1))
                sub_late_days -= extension_days
                sub_late_days = max(sub_late_days, 0)
                    
                if sub_late_days <= remaining_late_days[nid] and sub_late_days <= hard_days[project_id]: 
                    latest_sub_dir = submission_dir
                    remaining_late_days[nid] -= sub_late_days
                    break
                    
            links_idx += 1
        
        grades.append(get_grade(project_id, nid, latest_sub_dir, submit_time, sub_late_days, extension_days, soft_days[project_id], remaining_late_days[nid])) 
        
    return grades


@route
@user
def get_late_days(user, event):
    user_email = user['email']
    student_email = event['student_email']
    topic = event['topic']

    # two parties should be able to view the late days:
    # 1. submitter(s)
    # 2. grader
    if not (user_email == student_email or is_grader(user)):
        return (500, 'not authorized to view')

    nid = student_email.split("@")[0]
    grades = extract_grades(nid)
    return (200, [grade["late_days"] for grade in grades])

