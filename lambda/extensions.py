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

import json, urllib, boto3, botocore, base64, datetime, time, html
import traceback, random, string
import zipfile, io
from collections import defaultdict as ddict
from bs4 import BeautifulSoup

from lambda_framework import *
from roster import *
from projects import *


def extension_path(email, project_id):
    return 'extensions/%s/%s.json' % (to_s3_key_str(project_id), to_s3_key_str(email))


@route
@grader
def project_get_extension(user, event):
    project_id = event['project_id']
    if not project_id in get_project_due_utc():
        return (500, 'please enter a valid project ID: ' + ', '.join(sorted(get_project_due_utc().keys())))

    email = event['net_id']
    if not '@' in email:
        email += NET_ID_EMAIL_SUFFIX

    try:
        response = s3().get_object(Bucket=BUCKET, Key=extension_path(email, project_id))
        row = json.loads(str(response['Body'].read(), 'utf-8'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            row = {'days': 0, 'error': None}
        else:
            raise e

    row["on_roster"] = email in get_roster_emails()
    return (200, row)


@route
@grader
def project_set_extension(user, event):
    project_id = event['project_id']
    if not project_id in get_project_due_utc():
        return (500, 'please enter a valid project ID: ' + ', '.join(sorted(get_project_due_utc().keys())))
    
    email = event['net_id']
    if not '@' in email:
        email += NET_ID_EMAIL_SUFFIX

    days = int(event['days'])

    row = {'days': days, 'approver': user['email']}
    response = s3().put_object(Bucket=BUCKET, Key=extension_path(email, project_id),
                               Body=bytes(json.dumps(row), 'utf-8'),
                               ContentType='text/json')
    return (200, 'success')
