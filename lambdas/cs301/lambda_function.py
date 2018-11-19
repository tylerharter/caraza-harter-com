import json, urllib, boto3, botocore, base64, time, traceback, random, string
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
        record = {
            'request': event,
            'response': result
        }
        firehose().put_record(DeliveryStreamName=FIREHOSE,
                              Record = {'Data': json.dumps(record) + "\n"})
    except Exception as e:
        result = error('Firehose Error: '+str(e) + ' '+traceback.format_exc())

    return result
