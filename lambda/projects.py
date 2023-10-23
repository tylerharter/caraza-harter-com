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

import json, urllib, boto3, botocore, base64, datetime, time, html, copy
import traceback, random, string
import zipfile, io
from collections import defaultdict as ddict
from bs4 import BeautifulSoup

from lambda_framework import *
from roster import *

def get_project_due_utc():
    projects = copy.copy(s3().read_cached_json('config.json')['deadlines'])
    for k in projects:
        # central time is 5-6 hours behind UTC time, so to be safe, we'll
        # always have the project due at 7am on a Thu
        projects[k] = datetime.datetime.strptime(projects[k], "%m/%d/%y") + datetime.timedelta(days=1, hours=7)
    return projects

MAX_SIZE_KB = 5*1024

########################################
# lookup S3 paths for various objects
########################################

def project_dir(email, project_id):
    '''Get location where submission should be saved'''
    return 'projects/%s/%s/' % (to_s3_key_str(project_id), to_s3_key_str(email))


def rating_dir(email, project_id):
    '''Get location where submission should be saved'''
    return 'ratings/%s/%s/' % (to_s3_key_str(project_id), to_s3_key_str(email))


def submission_dir(email, project_id, submission_id):
    '''Get location where submission should be saved'''
    return '%s%s/' % (project_dir(email, project_id), submission_id)


def submission_path(email, project_id, submission_id):
    return submission_dir(email, project_id, submission_id) + "submission.json"


def submission_link(email, project_id, submission_id):
    return project_dir(email, project_id) + submission_id + "-link.json"


def cr_path(email, project_id, submission_id):
    return submission_dir(email, project_id, submission_id) + "cr.json"


def project_summary_path(email):
    '''Get location where summary of projects should be saved'''
    return 'projects/summary/%s.json' % to_s3_key_str(email)


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


def sanitize_html(page):
    '''safely transcribe HTML tables, and escape all else to make sure we never get potentially dangerous JS code'''
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.find_all('table')
    if len(tables) != 1:
        return html.escape(page)

    # there is one table, let's sanitize it
    t = tables[0]
    cells = {}
    for row, tr in enumerate(t.find_all("tr")):
        for col, td in enumerate(tr.find_all(["td", "th"])):
            cells[row,col] = td.get_text()

    rows, cols = max(cells)
    page = '<table border="1" cellspacing="0">\n' 
    for row in range(rows+1):
        page += "\t<tr>\n"
        for col in range(cols+1):
            tag = 'th' if (row==0 or col==0) else 'td'
            page += "\t\t<%s>\n" % tag
            page += "\t\t\t"
            page += html.escape(cells.get((row,col), ""))
            page += "\n"
            page += "\t\t</%s>\n" % tag
        page += "\t</tr>\n"
    page += "</table>\n"
    return page


def nb_cell_output_html(cell):
    '''Convert all ipython cell outputs to HTML'''

    outputs = cell.get('outputs', [])

    parts = []
    for output in outputs:
        output_type = output.get("output_type", "unknown")
        if output_type in ("execute_result", "display_data"):
            data = output.get("data", {})
            png = data.get("image/png", None)
            web = data.get("text/html", None)
            plain = data.get("text/plain", None)
            if png:
                parts.append('<img src="data:image/png;base64, {}"/>'.format(html.escape(png.strip())))
            elif web:
                parts.append(sanitize_html("".join(web)))
            elif plain:
                parts.append(html.escape("".join(plain)))
            else:
                parts.append("RAW-1: " + html.escape(str(output)))
        elif output_type == "stream":
            text = "".join(output.get("text", []))
            parts.append("<pre>" + html.escape(text) + "</pre>")
        else:
            parts.append("RAW-2: " + html.escape(str(output)))

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
        # TODO: what if the .zip contains a .ipynb?
        try:
            z = zipfile.ZipFile(io.BytesIO(binary_bytes), 'r')
            for filename in z.namelist():
                if filename.endswith(('.py', '.html', '.csv')):
                    try:
                        code = normalize_py_bytes(z.read(filename))

                        if filename.endswith(".csv"):
                            lines = code.split("\n")
                            line_count = len(lines)
                            if line_count > 30:
                                lines = lines[:10] + lines[-10:]
                                lines.insert(10, "\n...%d more lines [HIDDEN]...\n" % (line_count-20))
                            code = "\n".join(lines)
                    except Exception as e:
                        code = 'could not read\n' # not everything in a zip should be readable, so this is fine
                    result['files'][filename] = code
                elif filename.endswith('.ipynb'):
                    nb = json.loads(str(z.read(filename), 'utf-8'))
                    cells = nb.get('cells', [])
                    for i,cell in enumerate(cells):
                        exec_count = cell.get('execution_count', None)
                        if exec_count == None:
                            exec_count = ' '

                        # we can't use ipython execution order as the ID, because some cells
                        # might not have been run (so they won't have an execution order)
                        # TODO: avoid repeats if multiple .ipynb files...
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
                elif filename.endswith('.svg'):
                    result['files'][filename] = f'<img src="data:image/svg+xml,{normalize_py_bytes(z.read(filename))}">'
                else:
                    result['files'][filename] = '...not code...'

        except Exception as e:
            result['errors'].append(str(e))
    return result


def get_code_analysis(student_email, project_id, project_files):
    pf = project_files
    comments = []
    analysis = {
        'comments': comments,
        'partner': None,
        'errors': False,
    }
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

    # extract these fields from comments:
    # submitter (should be an email)
    # partner (should be an email or "none")
    # project (p1, p2, etc)
    # hours (estimate of how long the project took
    fields = {'project':set(), 'submitter':set(), 'partner':set(), 'hours':set()}
    for filename in pf['files'].keys():
        # check .py files and nb cells
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
    if student_email != None:
        if not student_email.lower().endswith(NET_ID_EMAIL_SUFFIX):
            comments.append('<b>error:</b> not submitted from an @wisc.edu account (%s)' % student_email)
            analysis['errors'] = True
        elif len(fields['submitter']) == 1:
            submitter = list(fields['submitter'])[0]
            if not "@" in submitter:
                submitter += NET_ID_EMAIL_SUFFIX
            if submitter != student_email:
                comments.append('<b>error:</b> expected submitter to be "%s", not "%s"' % (student_email, submitter))
                analysis['errors'] = True

    # check partner is on the roster (if partners are enabled)
    if s3().read_cached_json('config.json').get("partners", True):
        if len(fields['partner']) == 1:
            partner = list(fields['partner'])[0]
            if partner.strip().lower() == "none":
                comments.append('info: no partner')
            else:
                if not '@' in partner:
                    partner += NET_ID_EMAIL_SUFFIX
                analysis['partner'] = partner
                if not partner in get_roster_emails():
                    comments.append('<b>error:</b> "%s" not on the roster' % partner)
                    analysis['errors'] = True
                else:
                    comments.append('info: partner is ' + partner)

    # check that hours is a number
    if len(fields['hours']) == 1:
        hours = list(fields['hours'])[0].strip()
        try:
            hours_float = float(hours)
            analysis['hours'] = hours_float
        except ValueError:
            comments.append('<b>hours:</b> "%s" not a number' % hours)
            analysis['errors'] = True

    # check that project is correct
    if len(fields['project']) == 1:
        project = list(fields['project'])[0]
        if project.lower().strip() != project_id.lower().strip():
            comments.append('<b>error:</b> expected project "%s" but found "%s"' % (project_id, project))
            analysis['errors'] = True

    return analysis


########################################
# route endpoints
########################################

@route
@user
def project_upload(user, event):
    user_email = user['email']
    project_id = event['project_id']
    ignore_errors = event.get('ignore_errors', True) # does user want to force a submission, despite errors?
    if not project_id in get_project_due_utc():
        return (500, 'not a valid project')

    if len(base64.b64decode(event['payload'])) > MAX_SIZE_KB*1024:
        return (500, 'file is too large')

    submission_id = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

    # compute late days (may be negative if it was early).  Negative
    # is only for our own information, though (it doesn't somehow
    # replenish the student's supply)
    late_days = 0
    utc_due = get_project_due_utc().get(project_id, None)
    utc_now = datetime.datetime.utcnow()
    if utc_due != None:
        late_seconds = (utc_now - utc_due).total_seconds()
        late_days = late_seconds / 60 / 60 / 24

    # try to fetch the formatted contents of the project so user can
    # preview without doing an S3 read
    project_files = extract_project_files(submission_id,
                                          event['filename'],
                                          event['payload'])

    analysis = get_code_analysis(user_email, project_id, project_files)

    # JSON blob to save to S3 bucket
    submission = {'project_id': project_id,
                  'submission_id': submission_id,
                  'due_time_utc': utc_due.strftime("%Y-%m-%d %H:%M:%S") if utc_due else None,
                  'submit_time_utc': utc_now.strftime("%Y-%m-%d %H:%M:%S") if utc_now else None,
                  'late_days': late_days,
                  'filename': event['filename'],
                  'payload': event['payload'],
                  'feedback_request': event['feedback_request'],
                  'partner_email': analysis['partner'],
                  'ignore_errors': ignore_errors}

    if ignore_errors or not analysis['errors']:
        path = submission_path(user_email, project_id, submission_id)
        s3().put_object(Bucket=BUCKET,
                        Key=path,
                        Body=bytes(json.dumps(submission), 'utf-8'),
                        ContentType='text/json')

        # create links for both partners to the submission
        sub_dir = submission_dir(user_email, project_id, submission_id)
        s3().s3_link(sub_dir, submission_link(user_email, project_id, submission_id))
        if submission['partner_email'] and user_email in get_roster_emails():
            s3().s3_link(sub_dir, submission_link(submission['partner_email'], project_id, submission_id))

    result = {'analysis': analysis}
    return (200, result)


@route
@user
def get_submission(user, event):
    '''Viewing a "code review" is the only way students view code.  Even
    previewing a submission is just viewing an empty code review with
    no highlights.'''

    user_email = user['email']
    student_email = event['student_email']
    project_id = event['project_id']

    # two parties should be able to view the code review:
    # 1. submitter(s)
    # 2. grader
    if not (user_email == student_email or is_grader(user)):
        return (500, 'not authorized to view that submission')

    # return list of ALL submissions for this project
    submissions = []
    for path in s3().s3_all_keys(project_dir(student_email, project_id)):
        name = path.split("/")[-1]
        suffix = '-link.json'
        if name.endswith(suffix):
            submissions.append({"id": name[:-len(suffix)]})
    result = {
        'is_grader': is_grader(user),
        'submissions': submissions
    }

    # embed details for one of the submissions for this project
    if len(submissions) > 0:
        submissions.sort(key=lambda s: s["id"], reverse=True)
        submission_id = event.get('submission_id', None)
        if not submission_id:
            submission_id = submissions[0]["id"]

        link = submission_link(student_email, project_id, submission_id)
        sub_dir = s3().read_json(link)["symlink"]
        result['submission_dir'] = sub_dir

        submission = s3().read_json(sub_dir + 'submission.json')
        code = extract_project_files(submission['submission_id'], submission['filename'], submission['payload'])

        result['submission_id'] = submission_id
        result['code'] = code
        result['payload'] = submission['payload']
        result['analysis'] = get_code_analysis(None, project_id, code)
        result['feedback_request'] = sanitize_html(submission.get('feedback_request', ''))

        # add details from test.json and cr.json, if they exist
        test_result = s3().read_json_default(sub_dir + 'test.json')
        if test_result:
            result['test_result'] = test_result
        result['cr'] = s3().read_json_default(sub_dir + 'cr.json')
        if result['cr'] == None:
            result['cr'] = {
                'highlights': {k:[] for k in code['files'].keys()}, # list of highlight ranges with comments
                'general_comments': '',      # comments about whole submission
                'points_deducted': 0,        # TAs can take additional points off
                'reviewer_email': None,      # who left the code review
            }

    return (200, result)


@route
@grader
def project_list_submissions(user, event):
    # get roster indexed by wiscmail
    roster = {student['net_id']+"@wisc.edu": student for student in get_roster_json() if 'net_id' in student}
    project_id = event['project_id']

    if not project_id in get_project_due_utc():
        return (500, 'invalid project id')
    paths = s3().s3_all_keys('projects/'+project_id+'/')

    # which TA is assigned to each student for this project?
    cr_assignments = s3().read_json_default('projects/%s-cr-assignments.json' % project_id, default={})

    # email => list of submission IDs
    submissions = ddict(list)
    direct_submissions = ddict(list)

    # emails of students who have recevied test results or CRs on some version of their code
    reviewed = set()
    tested = set()

    for path in paths:
        parts = path.split('/')

        # Example:
        # projects/p2/tylerharter*at*gmail.com/2019-08-16_17-58-37/submission.json (len=5)
        # projects/p2/tylerharter*at*gmail.com/2019-08-16_17-58-37-link.json (len=4)

        if len(parts) > 2:
            email = parts[2].replace("*at*", "@")
        
        if len(parts) == 5 and parts[-1] == 'submission.json':
            direct_submissions[email].append(parts[3])

        if len(parts) == 5 and parts[-1] == 'cr.json':
            reviewed.add(email)

        if len(parts) == 5 and parts[-1] == 'test.json':
            tested.add(email)

        link_suffix = '-link.json'
        if len(parts) == 4 and parts[-1].endswith(link_suffix):
            submissions[email].append(parts[3][:-len(link_suffix)])

    # we only want links to submissions that have been directly
    # submitted (in contrast to submissions submitted by a partner),
    # so we don't review the same thing twice.
    #
    # we're also only interested in the most recent submission
    rows = []
    for email in direct_submissions:
        latest_direct = max(direct_submissions[email])

        if len(submissions[email]) == 0:
            # this should only happen if lambda crashed between S3 writes, or a submission is withdrawn
            continue

        latest = max(submissions[email])
        if latest_direct != latest:
            continue # this direct submission has been superceded by a partner's more-recent submission

        row = {
            'project_id': project_id,
            'student_email': email,
            'submission_id': latest_direct,
            'has_review': email in reviewed,
            'tested': email in tested,
            'info': {},
        }

        # supplement with info from roster (do we still need this?)
        row['info']['net_id'] = roster.get(email,{}).get('net_id',None)

        # supplement with info about the assigned grader
        row['info']['ta'] = cr_assignments.get(email, None)

        rows.append(row)

    return (200, {'submissions': rows, 'reviewed': list(reviewed), 'direct': list(direct_submissions.keys())})


@route
@grader
def put_code_review(user, event):
    cr = event['cr']
    cr['reviewer_email'] = user['email']
    sub_dir = event['submission_dir']
    if not sub_dir.endswith('/'):
        return (500, 'bad sub_dir "%s"' % sub_dir)

    s3().put_object(Bucket=BUCKET,
                    Key=sub_dir + 'cr.json',
                    Body=bytes(json.dumps(cr), 'utf-8'),
                    ContentType='text/json')

    return (200, 'uploaded review')


@route
@user
def project_get_summary(user, event):
    user_email = user['email']

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
    if not (user_email == student_google_id or is_grader(user)):
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


@route
@user
def rate_comment(user, event):
    user_email = user['email']
    rating = {k: event['rating'].get(k, None) for k in
              ("reviewer", "project_id", "submission_dir", "filename", "offset", "length", "comment", "useful")}
    if not rating['project_id'] in get_project_due_utc():
        return (500, 'not a valid project')
    rating_id = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    path = rating_dir(user_email, rating['project_id']) + rating_id + '.json'
    s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(rating), 'utf-8'),
                    ContentType='text/json',
    )
    return (200, 'rating recorded')
