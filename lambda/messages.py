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

@route
@user
def get_message(user, event):
    user_email = user['email']
    student_email = event['student_email']
    topic = event['topic']

    # two parties should be able to view the code review:
    # 1. submitter(s)
    # 2. grader
    if not (user_email == student_email or is_grader(user)):
        return (500, 'not authorized to view')

    path = 'messages/%s/%s.json' % (to_s3_key_str(student_email), topic)
    msg = s3().read_json_default(path, default={"subject": "Message Not Found", "msg": "do you have the right URL?", "path": path})
    return (200, msg)

