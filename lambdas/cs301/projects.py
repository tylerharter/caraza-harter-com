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

import json, urllib, boto3, botocore, base64, datetime, time, html
import traceback, random, string
import zipfile, io
from collections import defaultdict as ddict

from lambda_framework import *
from roster import *

PROJECT_IDS = [
    'p1', 'p2', 'p3', 'p4', 'p5', 'p6',
    'p7', 'p8', 'p9', 'p10'
]

# central time is 5-6 hours behind UTC time, so to be safe, we'll
# always have the project due at 7am on a Thu
DUE_DATE_FORMAT = "%m/%d/%y %H:%M"
PROJECT_DUE_UTC = {
    'p1':  datetime.datetime.strptime("01/31/19 7:00", DUE_DATE_FORMAT),
    'p2':  datetime.datetime.strptime("02/07/19 7:00", DUE_DATE_FORMAT),
    'p3':  datetime.datetime.strptime("02/14/19 7:00", DUE_DATE_FORMAT),
    'p4':  datetime.datetime.strptime("02/21/19 7:00", DUE_DATE_FORMAT),
    'p5':  datetime.datetime.strptime("02/28/19 7:00", DUE_DATE_FORMAT),
    'p6':  datetime.datetime.strptime("03/07/19 7:00", DUE_DATE_FORMAT),
    'p7':  datetime.datetime.strptime("03/14/19 7:00", DUE_DATE_FORMAT),
    'p8':  datetime.datetime.strptime("04/04/19 7:00", DUE_DATE_FORMAT),
    'p9':  datetime.datetime.strptime("04/18/19 7:00", DUE_DATE_FORMAT),
    'p10': datetime.datetime.strptime("05/04/19 7:00", DUE_DATE_FORMAT),
}

MAX_SIZE_KB = 1024

########################################
# lookup S3 paths for various objects
########################################

def project_path(user_id, project_id, submission_id=None):
    '''Get location where submission should be saved'''
    path = 'projects/%s/users/%s/' % (project_id, user_id)
    path += (submission_id if submission_id != None else 'curr.json')
    return path


def project_summary_path(user_id):
    '''Get location where summary of projects should be saved'''
    return 'projects/summary/users/%s.json' % user_id


def code_review_path(user_id, project_id, cr_id=None):
    name = 'cr%s.json' % ("-"+str(cr_id) if cr_id != None else "")
    return 'projects/%s/users/%s/%s' % (project_id, user_id, name)


def extension_path(user_id, project_id):
    return 'projects/%s/users/%s/extension.json' % (project_id, user_id)


def partner_path(user_id, project_id):
    return 'projects/%s/users/%s/partner.json' % (project_id, user_id)


########################################
# other helpers
########################################

def normalize_py_bytes(b):
    '''take a binary string, and force to be an ascii string with UNIX newlines'''
    code = str(b, 'utf-8') # assume a .py is utf-8
    # force to ascii
    code = str(bytes(code, 'ascii', 'replace'), 'ascii')
    # normalize windows line endings to UNIX
    code = code.replace("\r\n", "\n")
    return code


def nb_cell_output_html(cell):
    '''Convert all ipython cell outputs to HTML'''

    outputs = cell.get('outputs', [])

    parts = []
    for output in outputs:
        data = output.get("data", {})
        png = data.get("image/png", None)
        web = data.get("text/html", None)
        plain = data.get("text/plain", None)
        if png:
            parts.append('<img src="data:image/png;base64, {}"/>'.format(png.strip()))
        elif web:
            parts.append("".join(web))
        elif plain:
            parts.append(html.escape("".join(plain)))
        else:
            parts.append(html.escape("<" + ",".join(map(str,data.keys()))) + ">")

    return '\n<br>\n'.join(parts)


def extract_project_files(submission_id, filename, payload):
    '''take a b64 payload, and extract all the files to different dict
    entries.  There will be one entry if it's a .py, and potentially
    many if it is a .zip'''

    result = {'submission_id':submission_id,
              'root':filename,
              'files': {},      # these may be whole .py files, or cells in a ipynb
              'files_meta': {},
              'errors': []}

    def add_file_meta(key, display_name, order, content_type):
        meta = {'display_name':display_name, 'order':order, 'content_type':content_type}
        result['files_meta'][key] = meta
    
    binary_bytes = base64.b64decode(payload)
    if filename.endswith('.py'):
        # format 1: a single .py file
        try:
            code = normalize_py_bytes(binary_bytes)
        except Exception as e:
            result['errors'].append(str(e))
            code = 'could not read\n'
        result['files'][filename] = code
    elif filename.endswith('.ipynb'):
        # format 2: a single python notebook
        nb = json.loads(str(binary_bytes, 'utf-8'))
        cells = nb.get('cells', [])
        for i,cell in enumerate(cells):
            exec_count = cell.get('execution_count', None)
            if exec_count == None:
                exec_count = ' '

            # we can't use ipython execution order as the ID, because some cells
            # might not have been run (so they won't have an execution order)
            inbox = 'in-%d' % (i + 1000)
            outbox = 'out-%d' % (i + 1000)

            # in cell
            result['files'][inbox] = ''.join(cell['source'])
            if result['files'][inbox] == '':
                result['files'][inbox] = '\n'
            add_file_meta(inbox, 'In [%s]'%str(exec_count), order=i, content_type='python')

            # out cell
            if len(cell.get('outputs', [])) > 0:
                result['files'][outbox] = nb_cell_output_html(cell)
                add_file_meta(outbox, 'Out[%s]'%str(exec_count), order=i, content_type='html')
    else:
        # format 3: a zip of .py files
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


def get_code_analysis(submitter_email, project_id, project_files):
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
    nb_cell_count = len([fn for fn in pf['files'].keys() if fn.startswith('in-')])
    comments.append('info: there were %d .py files submitted' % code_file_count)
    comments.append('info: there were %d notebook cells' % nb_cell_count)

    # extract various fields from comments
    fields = {'project':set(), 'submitter-netid':set(), 'partner-netid':set()}

    for filename in pf['files'].keys():
        # look in .py files and ipython notebook cells (which are innapropriately named files here)
        if not (filename.endswith('.py') or filename.startswith('in-')):
            continue
        code = pf['files'][filename]

        for line in code.split('\n'):
            line = line.strip().lower()
            if not line.startswith('#'):
                continue
            parts = list(map(str.strip, line[1:].split(':')))

            if len(parts) == 2:
                if parts[0] in fields:
                    fields[parts[0]].add(parts[1])

    # check that we were given exactly one value for each field
    for key in fields:
        if len(fields[key]) == 0:
            comments.append('<b>error:</b> no value specified for "%s"' % key)
            analysis['errors'] = True
        elif len(fields[key]) > 1:
            comments.append('<b>error:</b> conflicting values specified for "%s": %s' % (key, ','.join(fields[key])))
            analysis['errors'] = True

    # check user's Net ID matches the comment in the code
    # (this check doesn't run if TA is fetching the CR)
    if submitter_email != None:
        parts = submitter_email.lower().split('@')
        if parts[-1] != 'wisc.edu':
            comments.append('<b>error:</b> not submitted from an @wisc.edu account')
            analysis['errors'] = True
        elif len(fields['submitter-netid']) == 1:
            submitter = list(fields['submitter-netid'])[0]
            if submitter.strip().lower() != parts[0].strip().lower():
                comments.append('<b>error:</b> expected submitter-netid to be "%s", not "%s"' % (parts[0], submitter))
                analysis['errors'] = True

    # check partner is on the roster
    if len(fields['partner-netid']) == 1:
        partner = list(fields['partner-netid'])[0]
        if partner.strip().lower() == "none":
            comments.append('info: no partner')
        elif not partner in get_roster_net_ids():
            comments.append('<b>error:</b> partner NetID %s not on the roster' % partner)
            analysis['errors'] = True
        else:
            comments.append('info: partner is ' + partner)
            analysis['partner'] = partner

    # TODO: check that project is correct
    if len(fields['project']) == 1:
        project = list(fields['project'])[0]
        if project.lower().strip() != project_id.lower().strip():
            comments.append('<b>error:</b> expected project "%s" but found "%s"' % (project_id, project))
            analysis['errors'] = True

    return analysis


def get_project_test_result(submitter_user_id, project_id):
    # get net ID
    path = 'users/google_to_net_id/%s.txt' % submitter_user_id
    try:
        response = s3().get_object(Bucket=BUCKET, Key=path)
        net_id = response['Body'].read().decode('utf-8')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return None
        raise e

    # get test result file (if any)
    result_path = 'ta/grading/{project_id}/{net_id}.json'
    result_path = result_path.format(project_id=project_id, net_id=net_id)
    try:
        response = s3().get_object(Bucket=BUCKET, Key=result_path)
        result = json.loads(response['Body'].read().decode('utf-8'))
        return result
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return None
        raise e


def get_code_review_raw(user, submitter_user_id, project_id,
                        force_new, project_files=None):
    """get code review blob from S3 or from project_files.

    user could be either the submitter, or a TA

    Sometimes a
    code upload calls this, so we have project_files without needing
    to look to S3.  If force_new is True, or there is no code review
    available, a new one is created"""

    submitter_email = None
    if user['sub'] == submitter_user_id:
        submitter_email = user['email']

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
        cr = {
            'submission_id': None,       # which submission is this associated with?
            'highlights': None,          # list of highlight ranges with comments
            'general_comments': '',      # comments about whole submission
            'points_deducted': 0,        # TAs can take additional points off
            'reviewer_email': None,      # who left the code review
        }

    # step 2: get associated code (if we don't have it)
    try:
        if project_files == None:
            project_files = load_project_from_s3(submitter_user_id, project_id,
                                                 submission_id=cr['submission_id'])
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return (500, 'no project submission found')
        return (500, str(e.response))

    # highlights
    if cr['highlights'] == None:
        # start with a clean slate (i.e., not highlights on any files)
        cr['highlights'] = {k:[] for k in project_files['files'].keys()}

    # these extra fields are auto-populated each time a CR is
    # requested, regardless of what might be saved in cr.json
    cr['submission_id'] = project_files['submission_id'] # resolve curr to actual ID
    cr['is_grader'] = is_grader(user)
    cr['project'] = project_files
    cr['analysis'] = get_code_analysis(submitter_email, project_id, project_files)
    cr['test_result'] = get_project_test_result(submitter_user_id, project_id)

    return (200, cr)


def lookup_partner_netid(user_id, project_id):
    path = partner_path(user_id, project_id)
    try:
        response = s3().get_object(Bucket=BUCKET, Key=path)
        row = json.loads(str(response['Body'].read(), 'utf-8'))
        return row.get('netid', None)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return None
        raise(e)


def project_list_submissions_raw(roster, project_id):
    roster = {student['user_id']: student for student in roster if 'user_id' in student}

    if not project_id in PROJECT_IDS:
        return (500, 'invalid project id')
    paths = s3_all_keys('projects/'+project_id+'/')

    # set of submitter_id's of user that have received code reviews
    reviewed = set()
    
    submissions = []
    for path in paths:
        parts = path.split('/')
        if (len(parts) != 5 or parts[0] != 'projects' or parts[2] != 'users'):
            continue

        submitter_id = parts[3]
        filename = parts[4]

        if filename == 'cr.json':
            reviewed.add(submitter_id)
        elif filename == 'curr.json':
            submission = {
                'project_id':project_id,
                'submitter_id':submitter_id,
                'info': {},
                'path': path
            }

            # supplement with info from roster
            for field in ['net_id', 'ta']:
                submission['info'][field] = roster.get(submitter_id,{}).get(field,None)
            submissions.append(submission)

    # augment submissions with info about reviews
    for submission in submissions:
        submission['has_review'] = (submission['submitter_id'] in reviewed)

    return (200, {'submissions':submissions})


########################################
# route endpoints
########################################

@route
def project_list(user, event):
    # no special permissions necessary
    return (200, PROJECT_IDS)


@route
@user
def project_upload(user, event):
    user_id = user['sub']
    project_id = event['project_id']
    ignore_errors = event.get('ignore_errors', True) # does user want to force a submission, despite errors?
    if not project_id in PROJECT_IDS:
        return (500, 'not a valid project')

    if len(base64.b64decode(event['payload'])) > MAX_SIZE_KB*1024:
        return (500, 'file is too large')

    submission_id = '%.2f' % time.time()

    # compute late days (may be negative if it was early).  Negative
    # is only for our own information, though (it doesn't somehow
    # replenish the student's supply)
    late_days = 0
    utc_due = PROJECT_DUE_UTC.get(project_id, None)
    utc_now = datetime.datetime.utcnow()
    if utc_due != None:
        late_seconds = (utc_now - utc_due).total_seconds()
        late_days = late_seconds / 60 / 60 / 24

    # try to fetch the formatted contents of the project so user can
    # preview without doing an S3 read
    project_files = extract_project_files(submission_id,
                                          event['filename'],
                                          event['payload'])
    rc,cr = get_code_review_raw(user, user_id, project_id,
                                force_new=True, project_files=project_files)
    if rc != 200:
        return (rc, "could not get CR")

    # save partner permissions
    path = partner_path(user_id, project_id)
    partner = {'netid': cr.get('analysis', {}).get('partner', None)}
    s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(partner), 'utf-8'),
                    ContentType='text/json')

    # JSON blob to save to S3 bucket
    submission = {'project_id': project_id,
                  'submission_id': submission_id,
                  'due_time_utc': utc_due.strftime("%Y-%m-%d %H:%M:%S") if utc_due else None,
                  'submit_time_utc': utc_now.strftime("%Y-%m-%d %H:%M:%S") if utc_now else None,
                  'late_days': late_days,
                  'filename': event['filename'],
                  'payload': event['payload'],
                  'partner_netid': cr['analysis']['partner'],
                  'ignore_errors': ignore_errors}

    paths = [project_path(user_id, project_id, submission_id)] # for history only
    if ignore_errors or not cr['analysis']['errors']:
        # we only do the main submission if there are no errors, or
        # the student chooses to ignore errors
        paths.append(project_path(user_id, project_id))

    for path in paths:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(submission), 'utf-8'),
                        ContentType='text/json')

    result = {'code_review': cr}
    return (200, result)


@route
@user
def project_withdraw(user, event):
    user_id = user['sub']
    project_id = event['project_id']
    if not project_id in PROJECT_IDS:
        return (500, 'not a valid project')

    path = project_path(user_id, project_id)
    s3().delete_object(Bucket=BUCKET, Key=path)
    result = {'message': 'project submission withdrawn'}
    return (200, result)


@route
@user
def get_code_review(user, event):
    '''Viewing a "code review" is the only way students view code.  Even
    previewing a submission is just viewing an empty code review with
    no highlights.'''

    user_id = user['sub']
    user_netid = google_to_net_id(user_id)
    submitter_user_id=event['submitter_id']
    project_id = event['project_id']
    partner_netid = lookup_partner_netid(submitter_user_id, project_id)
    force_new = event.get('force_new', False)

    # three people should be able to view the code review:
    # 1. submitter
    # 2. project partner
    # 3. grader

    if not (user_id == submitter_user_id or
            (user_netid != None and user_netid == partner_netid) or
            is_grader(user)):
        return (500, 'not authorized to view that submission')

    return get_code_review_raw(user=user,
                               submitter_user_id=submitter_user_id,
                               project_id=project_id,
                               force_new=force_new)


@route
@grader
def put_code_review(user, event):
    cr = event['cr']
    project_id = event['project_id']
    cr['reviewer_email'] = user['email']
    if not project_id in PROJECT_IDS:
        return (500, 'not a valid project')
    submitter_user_id = event['submitter_id']

    cr_id = '%.2f' % time.time()
    for path in [code_review_path(submitter_user_id, project_id),
                 code_review_path(submitter_user_id, project_id, cr_id)]:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(cr), 'utf-8'),
                        ContentType='text/json',
        )
    return (200, 'uploaded review')


@route
@admin
def resync_partner_id(user, event):
    """This is a consistency tool.  If somehow partner wasn't recorded
    upon submission, we can try again now.  Until there is a user
    interface, you can paste the following in the JS console:

    common.callLambda({"fn":"resync_partner_id", "project_id":"????", "submitter_user_id":"????"}, function(d) {console.log(d)}, function(d) {console.log(d)})
    """

    submitter_user_id = event['submitter_user_id']
    project_id = event['project_id']

    # update partner.json
    project_files = load_project_from_s3(submitter_user_id, project_id)
    analysis = get_code_analysis(None, project_id, project_files)
    partner = {'netid': analysis.get('partner', None)}
    path = partner_path(submitter_user_id, project_id)
    s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(partner), 'utf-8'),
                    ContentType='text/json')

    # update curr.json
    response = s3().get_object(Bucket=BUCKET, Key=project_path(submitter_user_id, project_id))
    submission = json.loads(str(response['Body'].read(), 'utf-8'))

    submission_id = '%.2f' % time.time()
    submission['partner_netid'] = partner['netid']
    for path in [project_path(submitter_user_id, project_id),
                 project_path(submitter_user_id, project_id, submission_id)]:
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(submission), 'utf-8'),
                        ContentType='text/json')

    return (200, json.dumps(partner))


@route
@grader
def project_list_submissions(user, event):
    roster = json.loads(get_roster_raw())
    return project_list_submissions_raw(roster, event['project_id'])


@route
@grader
def project_get_extension(user, event):
    project_id = event['project_id']
    if not project_id in PROJECT_IDS:
        return (500, 'please enter a valid project ID: ' + ', '.join(PROJECT_IDS))
    student_user_id = net_id_to_google(event['net_id'])
    if student_user_id == None:
        return (500, 'could not find google ID for net ID')
    path = extension_path(student_user_id, project_id)

    try:
        response = s3().get_object(Bucket=BUCKET, Key=path)
        row = json.loads(str(response['Body'].read(), 'utf-8'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            row = {'days': 0, 'error': None}
        else:
            raise e
    return (200, row)


@route
@grader
def project_set_extension(user, event):
    project_id = event['project_id']
    if not project_id in PROJECT_IDS:
        return (500, 'please enter a valid project ID: ' + ', '.join(PROJECT_IDS))
    student_user_id = net_id_to_google(event['net_id'])
    days = int(event['days'])
    if student_user_id == None:
        return (500, 'could not find google ID for net ID')
    path = extension_path(student_user_id, project_id)

    row = {'days': days, 'approver': user['email']}
    response = s3().put_object(Bucket=BUCKET, Key=path,
                               Body=bytes(json.dumps(row), 'utf-8'),
                               ContentType='text/json')
    return (200, 'success')


@route
@user
def project_get_summary(user, event):
    user_id = user['sub']

    # get google id of student, directly, or from net_id
    student_google_id = event.get('google_id', None)
    if student_google_id == None:
        student_net_id = event.get('net_id', None)
        if student_net_id == None:
            return (500, 'must provide google_id or net_id')
        student_google_id = net_id_to_google(student_net_id)

    # two people should be able to view the project summary:
    # 1. student
    # 3. grader
    if not (user_id == student_google_id or is_grader(user)):
        return (500, 'not authorized to view this content')

    if student_google_id == None:
        return (500, 'could not find google user')

    path = project_summary_path(student_google_id)
    try:
        response = s3().get_object(Bucket=BUCKET, Key=path)
        row = json.loads(str(response['Body'].read(), 'utf-8'))
        row['path'] = path
        return (200, row)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            raise Exception("no status snapshot available")
        raise e
