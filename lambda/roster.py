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

from lambda_framework import *

NET_ID_EMAIL_SUFFIX = '@wisc.edu'

# returns a string containing json
def get_roster_raw():
    response = s3().get_object(Bucket=BUCKET, Key='roster.json')
    return response['Body'].read().decode('utf-8')


# TODO: index by class
emails = None
emails_updated = None
def get_roster_emails():
    global emails, emails_updated
    if emails != None and time.time() - emails_updated < 300:
        return emails
    emails = set()
    for row in json.loads(get_roster_raw()):
        if 'net_id' in row:
            emails.add(row['net_id'] + NET_ID_EMAIL_SUFFIX)
    emails_updated = time.time()
    return emails


@route
@admin
def get_roster(user, event):
    return (200, {'roster': get_roster_raw()})


@route
@admin
def put_roster(user, event):
    global emails
    emails = None
    body = json.dumps(json.loads(event['roster']), indent=2)
    s3().put_object(Bucket=BUCKET,
                    Key='roster.json',
                    Body=bytes(body, 'utf-8'),
                    ContentType='text/json',
    )

    return (200, 'roster uploaded')
