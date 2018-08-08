import json, urllib, boto3, botocore, base64, time, traceback, random, string
from collections import defaultdict as ddict

from lambda_framework import *

PROJECTS = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
MAX_SIZE_KB = 40

@route
def project_list(user, event):
    return (200, PROJECTS)

@route
@user
def project_upload(user, event):
    user_id = user['sub']
    project = event['project']
    if not project in PROJECTS:
        return (500, 'not a valid project')

    if len(base64.b64decode(event['payload'])) > MAX_SIZE_KB*1024:
        return (500, 'file is too large')
    
    row = {'project': project,
           'filename': event['filename'],
           'payload': event['payload']}

    submission_id = '%.2f' % time.time()
    root = 'projects/%s/%s' % (user_id, project)
    for path in [root+'/%s.json'%submission_id,
                 root+'/curr.json']:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(row), 'utf-8'),
                        ContentType='text/json',
        )
    return (200, {'message': 'project submitted'})

@route
@user
def project_view(user, event):
    user_id = user['sub']
    project = event['project']
    if not project in PROJECTS:
        return (500, 'not a valid project')
    path = 'projects/%s/%s/curr.json' % (user_id, project)
    response = s3().get_object(Bucket=BUCKET, Key=path)
    row = json.loads(str(response['Body'].read(), 'utf-8'))
    project = {'root':row['filename'], 'files': {}, 'errors': []}
    if row['filename'].endswith('.py'):
        try:
            body = str(base64.b64decode(row['payload']), 'utf-8')
            # force to ascii
            body = str(bytes(body, 'ascii', 'replace'), 'ascii')
            # normalize windows line endings to UNIX
            body = body.replace("\r\n", "\n")
        except Exception as e:
            row['errors'].append(str(e))
            body = 'could not read\n'
        project['files'][row['filename']] = body
    else:
        pass # TODO: parse zip
    return (200, project)
