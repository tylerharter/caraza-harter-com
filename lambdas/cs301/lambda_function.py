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

    # invoke
    fn = ROUTES.get(event['fn'], None)

    if fn == None:
        return error('no route for '+event['fn'])
    try:
        for checker in EXTRA_AUTH[event['fn']]:
            checker(user)
        code, data = fn(user, event)
    except Exception as e:
        return error('Exception: '+str(e) + ' '+traceback.format_exc())

    # result
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {},
        "body": data
    }
