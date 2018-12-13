import os, sys, json, math, datetime, boto3
from collections import defaultdict as ddict

BUCKET = 'caraza-harter-cs301'
s3 = boto3.client('s3')

TEST_NET_IDS = None
#TEST_NET_IDS = ['tharter']

LATE_DAY_ALLOCATION = 10

def gen_html(prows, include_intro=True):
    cum_late = 0

    intro = """<p>
    Dear Student,
    </p>

    <p>If anything looks wrong through P9, please let me
    (tylerharter@gmail.com) know by this <b>Wed, Dec 12th</b>.
    Otherwise, we'll assume you agree with the below summary when we
    compute final grades.</p>

    <p>There are MANY students with zeros due to improperly formatted
    Net IDs (directions here:
    https://tyler.caraza-harter.com/cs301/fall18/projects.html) as
    well as MANY zeros due to resubmissions where an extension wasn't
    recorded (you need to ask your reviewer to submit a deadline
    override if you were given permission to submit a fix).  There are
    also a few cases where people submitted as the wrong project
    (e.g., submitting P9 as P8), leading to getting zeros on both
    projects.</p>

    <p>I really don't want anybody to lose points over anything silly
    (like the above examples), but the semester is almost over, so now
    is the time to clear anything up.  So please don't wait to speak
    up.</p>

    <p>Here is your project summary:</p>
    """

    if include_intro:
        html = intro.split('\n')
    else:
        html = ['<h1>']

    for p in prows:
        html.append('<h2>' + p['project'].upper() + '</h2>')
        html.append('<ul>')
        line = '<li>Feedback: <a href="{}">{} reviewer comments</a>'
        html.append(line.format(p['code_review_url'], p['comment_count']))
        html.append('<li>Score: ' + str(p['score']))
        if p['override']:
            html[-1] += ' [override]'
        html.append('<li>Days Late: ' + str(p['late_days']))

        # handle late days
        cum_late += p['late_days']
        if (cum_late > LATE_DAY_ALLOCATION and p['late_days'] > 0):
            print('dropping projects because late!')
            html.append("<li>WARNING: late days exhausted ({} used to this point). ".format(cum_late) +
                        "This won't be counted. "+
                        "Please email your instructor to discuss.")

        html.append('</ul>')
    return '\n'.join(html)

def main():
    if len(sys.argv) < 3:
        print('Usage: python project_summary.py <project_id1> [<project_id2> ...]')
        sys.exit(1)

    projects = ddict(list)

    # group rows by net_id
    for project_id in sys.argv[1:]:
        with open('grades/'+project_id+'.json') as f:
            for row in json.load(f):
                projects[row['net_id']].append(row)

    # status by net_id
    net_ids = TEST_NET_IDS if TEST_NET_IDS != None else projects.keys()
    emails = []
    now = datetime.datetime.now()

    for net_id in net_ids:
        prows = projects[net_id]
        prows.sort(key=lambda row: int(row['project'][1:]))
        html = gen_html(prows)

        # distribute as email
        email = {'to':net_id+'@wisc.edu',
                 'subject': 'CS 301: Project Summary',
                 'message':html, 'html':True}
        emails.append(email)

        # generate status page in S3
        user_id = prows[0]['user_id']
        if user_id != None:
            path = 'projects/summary/users/%s.json' % user_id
            html_summary = gen_html(prows, include_intro=False)
            s3.put_object(Bucket=BUCKET,
                          Key=path,
                          Body=bytes(json.dumps({'when': str(now), 'html_summary': html_summary}), 'utf-8'),
                          ContentType='text/json')

    # dump email file
    with open('project_emails.json', 'w') as f:
        json.dump(emails, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
