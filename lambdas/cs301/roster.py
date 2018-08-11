import json, random

from lambda_framework import *

# returns a string containing json
def get_roster_raw():
    response = s3().get_object(Bucket=BUCKET, Key='users/roster.json')
    return response['Body'].read().decode('utf-8')

# takes a dict to convert to json
def put_roster_raw(roster_dict):
    body = json.dumps(roster_dict, indent=2)
    s3().put_object(Bucket=BUCKET,
                    Key='users/roster.json',
                    Body=bytes(body, 'utf-8'),
                    ContentType='text/json',
    )
    return body

@route
@admin
def get_roster(user, event):
    return (200, {'roster': get_roster_raw()})

@route
@admin
def put_roster(user, event):
    put_roster_raw(json.loads(event['roster']))
    return (200, 'roster uploaded')

@route
@admin
def roster_gen_link_codes(user, event):
    roster = json.loads(get_roster_raw())
    for student in roster:
        code = student.get('link_code', None)
        if code == None or event.get('overwrite_existing', False):
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        student['link_code'] = code
    body = put_roster_raw(roster)
    return (200, {'roster': body})

def roster_attach_user_raw(user_id, cs_login):
    path1 = 'users/google_to_cs_login/%s.txt' % user_id
    if s3_path_exists(path1):
        return (500, 'google account already linked to cs login')

    path2 = 'users/cs_login_to_google/%s.txt' % cs_login
    if s3_path_exists(path2):
        return (500, 'cs login already linked to google account')

    # if only one of these succeeds, it will require manual cleanup in S3
    s3().put_object(Bucket=BUCKET,
                    Key=path1,
                    Body=bytes(cs_login, 'utf-8'),
                    ContentType='text/json',
    )
    s3().put_object(Bucket=BUCKET,
                    Key=path2,
                    Body=bytes(user_id, 'utf-8'),
                    ContentType='text/json',
    )
    return (200, 'google account linked to cs login')

@route
@user
def roster_attach_user(user, event):
    user_id = user['sub']
    code = event['link_code']
    roster = json.loads(get_roster_raw())
    for student in roster:
        cs_login = student.get('cs_login', None)
        code2 = student.get('link_code', None)
        if cs_login != None and code2 != None and code == code2:
            return roster_attach_user_raw(user_id, cs_login)
    return (500, 'could not find student entry for that one-time link code')

@route
@user
def get_cs_login(user, event):
    user_id = user['sub']
    path = 'users/google_to_cs_login/%s.txt' % user_id
    try:
        # extract cs_login as plain text
        response = s3().get_object(Bucket=BUCKET, Key=path)
        cs_login = response['Body'].read().decode('utf-8')
    except botocore.exceptions.ClientError as e:
        # not linked yet
        if e.response['Error']['Code'] == "NoSuchKey":
            return (200, {"cs_login": None})
        # some unexpected error
        raise e

    # verify it points back to this user_id
    try:
        response = s3().get_object(Bucket=BUCKET, Key='users/cs_login_to_google/%s.txt' % cs_login)
        user_id_check = response['Body'].read().decode('utf-8')
        if user_id != user_id_check:
            return (500, 'google/cs linkage mismatch, please contact your instructor for help (1)')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return (500, 'google/cs linkage mismatch, please contact your instructor for help (2)')
        # some unexpected error
        raise e

    return (200, {"cs_login": cs_login})

@route
@admin
def roster_merge_google_ids(user, event):
    '''
    Look at individual files that link cs logins to google IDs and add
    that information to the main roster file for fast lookup.
    '''
    suffix = '.txt'
    all_files = s3_all_keys('users/cs_login_to_google/')
    linked_users = {path.split('/')[-1][:-4]
                    for path in all_files
                    if path.endswith('.txt')}

    roster = json.loads(get_roster_raw())
    for student in roster:
        user_id = student.get('user_id', None)
        cs_login = student.get('cs_login', None)
        # see if there's a link file with data we could roll into the main roster
        if user_id == None and cs_login in linked_users:
            path = 'users/cs_login_to_google/%s.txt' % cs_login
            response = s3().get_object(Bucket=BUCKET, Key=path)
            user_id = response['Body'].read().decode('utf-8')
            student['user_id'] = user_id
    body = put_roster_raw(roster)
    return (200, {'roster':body})
