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
def get_roster_json():
    return s3().read_cached_json('roster.json')


email_cache = {}
def get_roster_emails():
    if s3().key_prefix in email_cache:
        return email_cache[s3().key_prefix]
    emails = set()
    for row in get_roster_json():
        if 'net_id' in row:
            emails.add(row['net_id'] + NET_ID_EMAIL_SUFFIX)
    email_cache[s3().key_prefix] = emails
    return emails


@route
@admin
def get_roster(user, event):
    return (200, {'roster': json.dumps(get_roster_json(), indent=2, sort_keys=True)})


@route
@admin
def put_roster(user, event):
    s3().write_cached_json("roster.json", json.loads(event['roster']))
    return (200, 'roster uploaded')


@route
@user
def roster_entry(user, event):
    email = user['email'].lower()
    parts = email.split("@")
    if parts[1] != "wisc.edu":
        return (500, 'not a wisc.edu email')
    net_id = parts[0]

    for row in get_roster_json():
        if row["net_id"] == net_id:
            if row["enrolled"]:
                return (200, row)
            else:
                return (500, "not on enrolled")                
    else:
        return (500, "not on roster")        
