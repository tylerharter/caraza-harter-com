import json, urllib, boto3, botocore, base64, time, traceback, random, string
import zipfile, io
from collections import defaultdict as ddict

from lambda_framework import *
from roster import *

PROJECT_IDS = [
    'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6',
    'p7', 'p8', 'p9', 'p10'
]
MAX_SIZE_KB = 40

def normalize_py_bytes(b):
    '''take a binary string, and force to be an ascii string with UNIX newlines'''
    code = str(b, 'utf-8') # assume a .py is utf-8
    # force to ascii
    code = str(bytes(code, 'ascii', 'replace'), 'ascii')
    # normalize windows line endings to UNIX
    code = code.replace("\r\n", "\n")
    return code

def project_path(user_id, project_id, submission_id=None):
    '''Get location where submission should be saved'''
    path = 'projects/%s/users/%s/' % (project_id, user_id)
    path += (submission_id if submission_id != None else 'curr.json')
    return path

def code_review_path(user_id, project_id):
    return 'projects/%s/users/%s/cr.json' % (project_id, user_id)

def extract_project_files(submission_id, filename, payload):
    '''take a b64 payload, and extract all the files to different dict
    entries.  There will be one entry if it's a .py, and potentially
    many if it is a .zip'''

    result = {'submission_id':submission_id,
              'root':filename,
              'files': {},
              'errors': []}

    binary_bytes = base64.b64decode(payload)
    if filename.endswith('.py'):
        try:
            code = normalize_py_bytes(binary_bytes)
        except Exception as e:
            result['errors'].append(str(e))
            code = 'could not read\n'
        result['files'][filename] = code
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
            result['errors'].append(str(e))
    return result

def load_project_from_s3(user_id, project_id, submission_id=None):
    '''
    Fetch project in human readable format, extracting content from
    plaintext code files inside zip packages.
    '''
    path = project_path(user_id, project_id, submission_id)
    print('try to open '+path)
    response = s3().get_object(Bucket=BUCKET, Key=path)
    row = json.loads(str(response['Body'].read(), 'utf-8'))

    project_files = extract_project_files(row['submission_id'],
                                          row['filename'], row['payload'])
    return project_files

@route
def project_list(user, event):
    return (200, PROJECT_IDS)

def get_code_analysis(project_files):
    pf = project_files
    comments = []
    analysis = {'comments': comments, 'partner': None, 'errors': False}
    error_count = len(pf['errors'])

    # comment on errors
    if error_count > 0:
        comments.append('there were %d errors processing your submission' % error_count)
        analysis['errors'] = True

    # comment on number of source files
    code_file_count = len([fn for fn in pf['files'].keys() if fn.endswith('.py')])
    comments.append('there were %d .py files submitted' % code_file_count)

    # extract partner
    partners = set()
    for filename in pf['files'].keys():
        if not filename.endswith('.py'):
            continue
        code = pf['files'][filename]
        for line in code.split('\n'):
            line = line.strip().lower()
            if not line.startswith('#'):
                continue
            parts = list(map(str.strip, line[1:].split(':')))
            if len(parts) == 2 and parts[0] == 'partner-login':
                partners.add(parts[1])
    if len(partners) == 0:
        comments.append('no partner identified in the comments in your code')
    elif len(partners) >= 2:
        comments.append('you can only have one partner, but multiple given: %s' %
                        (', '.join(list(partners))))

        analysis['errors'] = True
    else:
        partner = list(partners)[0]
        net_ids = get_roster_net_ids()
        if not partner in net_ids:
            comments.append('partner NetID %s not on the roster' % partner)
            analysis['errors'] = True
        else:
            comments.append('partner: ' + partner)
            analysis['partner'] = partner

    return analysis

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

    # try to fetch the formatted contents of the project so user can
    # preview without doing an S3 read
    project_files = extract_project_files(submission_id,
                                          event['filename'],
                                          event['payload'])
    rc,cr = get_code_review_raw(user, user_id, project_id,
                                force_new=True, project_files=project_files)
    if rc != 200:
        cr = None

    # save project submission to S3 bucket
    submission = {'project_id': project_id,
                  'submission_id': submission_id,
                  'filename': event['filename'],
                  'payload': event['payload'],
                  'partner_netid': cr['analysis']['partner']}
    for path in [project_path(user_id, project_id),
                 project_path(user_id, project_id, submission_id)]:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(submission), 'utf-8'),
                        ContentType='text/json')

    result = {'message': 'project submitted', 'code_review': cr}
    return (200, result)

@route
@user
def get_partner(user, event):
    return (500, 'not implemented yet')

def get_code_review_raw(user, submitter_user_id, project_id,
                        force_new, project_files=None):
    user_id = user['sub']
    if submitter_user_id == None:
        submitter_user_id = user_id # assume self
    if user_id != submitter_user_id:
        # only graders can view the code of other users
        if not is_grader(user):
            return (500, 'not authorized to view that submission')

    # step 1: try to get CR unless we're forced to get a clean one on the latest submission
    cr = None
    if not force_new:
        try:
            response = s3().get_object(Bucket=BUCKET, Key=code_review_path(submitter_user_id, project_id))
            cr = json.loads(str(response['Body'].read(), 'utf-8'))
        except:
            pass

    # create a new empty CR if necessary
    if cr == None:
        cr = {'submission_id':None, 'ready':False, 'highlights':None}

    # step 2: get associated code
    try:
        if project_files == None:
            project_files = load_project_from_s3(submitter_user_id, project_id,
                                                 submission_id=cr['submission_id'])
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return (500, 'no project submission found')
        return (500, str(e.response))

    cr['submission_id'] = project_files['submission_id'] # resolve curr to actual ID
    cr['project'] = project_files
    cr['is_grader'] = is_grader(user)
    if cr['highlights'] == None:
        # start with a clean slate (i.e., not highlights on any files)
        cr['highlights'] = {k:[] for k in project_files['files'].keys()}
    cr['analysis'] = get_code_analysis(project_files)
        
    return (200, cr)

@route
@user
def get_code_review(user, event):
    '''Viewing a "code review" is the only way students view code.  Even
    previewing a submission is just viewing an empty code review with
    no highlights.'''
    force_new = event.get('force_new', False)
    return get_code_review_raw(user=user, submitter_user_id=event['submitter_id'],
                               project_id=event['project_id'],
                               force_new=force_new)

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

@route
@grader
def project_list_submissions(user, event):
    # get partial roster indexed by google IDs
    roster = json.loads(get_roster_raw())
    roster = {student['user_id']: student for student in roster if 'user_id' in student}

    project_id = event['project_id']
    if not project_id in PROJECT_IDS:
        return (500, 'invalid project id')
    paths = s3_all_keys('projects/'+project_id+'/')
    submissions = []
    for path in paths:
        parts = path.split('/')
        if (len(parts) != 5 or parts[0] != 'projects' or
            parts[2] != 'users' or parts[4] != 'curr.json'):
            continue
        submitter_id = parts[3]
        submission = {'project_id':project_id, 'submitter_id':submitter_id, 'info': {},
                      'path': path}
        for field in ['net_id', 'ta']:
            submission['info'][field] = roster.get(submitter_id,{}).get(field,None)
        submissions.append(submission)
    return (200, {'submissions':submissions})
