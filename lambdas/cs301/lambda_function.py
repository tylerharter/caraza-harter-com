import json, urllib, boto3, botocore, base64, time, traceback, random, string, copy
from collections import defaultdict as ddict

from lambda_framework import *
from clicker import *
from projects import *
from roster import *

def lambda_handler(event, context):
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
    try:
        record = log_record(event, result)
        firehose().put_record(DeliveryStreamName=FIREHOSE,
                              Record = {'Data': json.dumps(record) + "\n"})
    except Exception as e:
        result = error('Firehose Error: '+str(e) + ' '+traceback.format_exc())

    return result


def log_record(event, response):
    record = {
        'request': copy.deepcopy(event),
        'response': copy.deepcopy(response)
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
