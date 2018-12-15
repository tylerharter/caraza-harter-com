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

import json, urllib, boto3, botocore, base64, time, traceback, random, string
from collections import defaultdict as ddict

from lambda_framework import *

@route
@instructor
def put_question(user, event):
    question_id = '%.2f' % time.time()
    question = {'id': question_id,
                'question': event['question'],
                'open_question': event.get('open_question', False)}
    for path in ['questions/%s.json'%question_id, 'questions/curr.json']:
        s3().put_object(Bucket=BUCKET,
                      Key=path,
                      Body=bytes(json.dumps(question, indent=2), 'utf-8'),
                      ContentType='text/json',
        )
    return (200, {'message': 'question saved'})

def get_question_raw():
    try:
        response = s3().get_object(Bucket=BUCKET, Key='questions/curr.json')
        txt = response['Body'].read().decode('utf-8')
        return json.loads(txt)
    except Exception as e:
        return None
@route
def get_question(user, event):
    path = 'questions/curr.json'
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')
    return (200, question)

@route
def answer(user, event):  
    question_id = event['question_id']
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')

    if user != None:
        user_check(user)
        user_id = user['sub']
    else:
        # user didn't authenticate; check if it's required
        if question.get('open_question', False):
            # use random ID
            user_id = 'anon-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        else:
            return (500, 'this question requires authentication')

    answer = event['answer']

    # is it current?
    if question_id != question['id']:
        return (500, 'question has changed, please refresh')

    entry = {'user_id':user_id, 'answer':answer}
    entryJSON = json.dumps(entry)
    entryB64 = str(base64.b64encode(bytes(entryJSON, 'utf-8')), 'utf-8')
    inlinepath = 'questions/%s/answers/%s' % (question_id, entryB64)

    if len(bytes(inlinepath, 'utf-8')) < 1000:
        path = inlinepath
        s3().put_object(Bucket=BUCKET,
                      Key=inlinepath,
                      Body=bytes(entryJSON, 'utf-8'),
                      ContentType='text/json',
        )
        return (200, {'message': 'answer saved to '+inlinepath})
    else:
        # TODO: save it, but not inline
        return (500, 'answer too long')

@route
@instructor
def get_answer_counts(user, event):
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')

    user_id = user['sub']
    path = 'questions/%s/answers' % question['id']

    # count answers/errors
    response = {'errors': ddict(int), 'answers': ddict(int)}

    for key in s3_all_keys(path):
        name = key.split('/')[-1]
        try:
            b = base64.b64decode(name)
            txt = str(b, 'utf-8')
            row = json.loads(txt)
            response['answers'][row['answer']] += 1
        except Exception as e:
            response['errors'][str(e)] += 1
            continue
    return (200, response)
