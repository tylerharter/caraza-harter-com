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

import json, urllib, boto3, botocore, base64, time, traceback, random, string, copy
from collections import defaultdict as ddict

from lambda_framework import *
from clicker import *
from projects import *
from roster import *

def lambda_handler(event, context):
    ts0 = datetime.datetime.utcnow().timestamp()

    # identify user
    try:
        user = get_user(event)
    except Exception as e:
        user = None
    if user != None:
        save_user_info(user)

    # try to invoke the function
    fn = ROUTES.get(event['fn'], None)
    if fn != None:
        try:
            # if a check fails, it will raise an exception
            for checker in EXTRA_AUTH[event['fn']]:
                checker(user)

            code, data = fn(user, event)
            result = {
                "isBase64Encoded": False,
                "statusCode": code,
                "headers": {},
                "body": data
            }
        except Exception as e:
            result = error('Exception: '+str(e) + ' '+traceback.format_exc())
    else:
        result = error('no route for '+event['fn'])

    # try to log the event
    ts1 = datetime.datetime.utcnow().timestamp()
    try:
        record = log_record(event, result, user, ts0, ts1)
        firehose().put_record(DeliveryStreamName=FIREHOSE,
                              Record = {'Data': json.dumps(record) + "\n"})
    except Exception as e:
        result = error('Firehose Error: '+str(e) + ' '+traceback.format_exc())

    return result


def log_record(event, response, user, ts0, ts1):
    record = {
        'request': copy.deepcopy(event),
        'response': copy.deepcopy(response),
        'user_id': user.get('sub', None) if not user is None else None,
        'ts0': ts0,
        'ts1': ts1,
    }

    # we don't want traces to be too lange.
    # Thus, we replace long strings anywhere in the recursive structure with None.
    # we record these replacements with in dropped.
    max_str_len = 64
    dropped = []

    def compact_structs(location, struct):
        """location is a tuple of keys (keys in dicts or indices in lists) from the record
        object to get to struct"""

        if isinstance(struct, dict):
            keys = struct.keys()
        elif isinstance(struct, list):
            keys = range(len(struct))
        else:
            return

        for key in keys:
            val = struct[key]
            sublocation = location+(key,)
            
            if isinstance(val, str) and len(val) > max_str_len:
                dropped.append({
                    "location": sublocation,
                    "length": len(val)
                })
                struct[key] = None
            else:
                compact_structs(sublocation, val)
    compact_structs((), record)
    record['dropped'] = dropped

    return record
