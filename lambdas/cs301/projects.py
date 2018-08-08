import json, urllib, boto3, botocore, base64, time, traceback, random, string
import zipfile, io
from collections import defaultdict as ddict

from lambda_framework import *

PROJECT_IDS = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
MAX_SIZE_KB = 40

# take a binary string, and force to be an ascii string with UNIX newlines
def normalize_py_bytes(b):
    code = str(b, 'utf-8') # assume a .py is utf-8
    # force to ascii
    code = str(bytes(code, 'ascii', 'replace'), 'ascii')
    # normalize windows line endings to UNIX
    code = code.replace("\r\n", "\n")
    return code

def project_path(user_id, project_id, submission_id=None):
    path = 'projects/%s/users/%s/' % (project_id, user_id)
    path += (submission_id if submission_id != None else 'curr.json')
    return path

def code_review_path(user_id, project_id):
    return 'projects/%s/users/%s/cr.json' % (project_id, user_id)

# get displayable version, excluding binary files
def load_project(user_id, project_id, submission_id=None):
    path = project_path(user_id, project_id, submission_id)
    response = s3().get_object(Bucket=BUCKET, Key=path)
    row = json.loads(str(response['Body'].read(), 'utf-8'))
    result = {'submission_id':row['submission_id'],
              'root':row['filename'],
              'files': {},
              'errors': []}

    binary_bytes = base64.b64decode(row['payload'])
    if row['filename'].endswith('.py'):
        try:
            code = normalize_py_bytes(binary_bytes)
        except Exception as e:
            result['errors'].append(str(e))
            code = 'could not read\n'
        result['files'][row['filename']] = code
    else:
        try:
            z = zipfile.ZipFile(io.BytesIO(binary_bytes), 'r')
            for filename in z.namelist():
                if filename.endswith('.py'):
                    try:
                        code = normalize_py_bytes(z.read(filename))
                    except Exception as e:
                        code = 'could not read\n'
                        result['errors'].append(str(e))
                    result['files'][filename] = code
                else:
                    result['files'][filename] = '...not code...'

        except Exception as e:
            row['errors'].append(str(e))
    return result

@route
def project_list(user, event):
    return (200, PROJECT_IDS)

@route
@user
def project_upload(user, event):
    user_id = user['sub']
    project_id = event['project_id']
    if not project_id in PROJECT_IDS:
        return (500, 'not a valid project')

    if len(base64.b64decode(event['payload'])) > MAX_SIZE_KB*1024:
        return (500, 'file is too large')

    submission_id = '%.2f' % time.time()
    row = {'project_id': project_id,
           'submission_id': submission_id,
           'filename': event['filename'],
           'payload': event['payload']}

    for path in [project_path(user_id, project_id),
                 project_path(user_id, project_id, submission_id)]:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(row), 'utf-8'),
                        ContentType='text/json',
        )
    return (200, {'message': 'project submitted'})

@route
@user
def get_partner(user, event):
    return (500, 'not implemented yet')

@route
@user
def get_code_review(user, event):
    user_id = user['sub']
    submitter_user_id = event['submitter_id']
    if submitter_user_id == None:
        submitter_user_id = user_id # assume self
    project_id = event['project_id']
    if user_id != submitter_user_id:
        # only graders can view the code of other users
        if not is_grader(user):
            return (500, 'not authorized to view that submission')

    # step 1: get CR
    cr = None
    if not event.get('force_new', False):
        try:
            response = s3().get_object(Bucket=BUCKET, Key=code_review_path(submitter_user_id, project_id))
            cr = json.loads(str(response['Body'].read(), 'utf-8'))
        except:
            pass

    # create a new empty CR
    if cr == None:
        cr = {'submission_id':None, 'ready':False, 'highlights':None}

    # step 2: get associated code
    try:
        project = load_project(submitter_user_id, project_id, submission_id=cr['submission_id'])
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return (500, 'no project submission found')
        return (500, str(e.response))

    cr['submission_id'] = project['submission_id'] # resolve curr to actual ID
    cr['project'] = project
    if cr['highlights'] == None:
        cr['highlights'] = {k:[] for k in project['files'].keys()} # start with none

    return (200, cr)

@route
@grader
def put_code_review(user, event):
    cr = event['cr']
    submitter_user_id = event['submitter_id']
    project_id = event['project_id']
    path = code_review_path(submitter_user_id, project_id)
    s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(cr), 'utf-8'),
                    ContentType='text/json',
    )

    return (200, 'uploaded review')
