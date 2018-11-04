import os, sys, json, math
from collections import defaultdict as ddict

TEST_NET_IDS = None
#TEST_NET_IDS = ['tharter']

LATE_DAY_ALLOCATION = 10

def gen_html(prows):
    cum_late = 0

    intro = """<p>
    Dear Student,
    </p>

    <p>We're going to start sending status emails (like this one) so
    you can see links to all your feedback and a summary of late days
    in one place.</p>

    <p>Most feedback comments we leave you are tips for how to write
    better code or simpler ways to do what you're trying to do.  So we
    strongly encourage you to read all TA comments, even if you scored
    100.  It will likely save you time in the future.</p>

    <p>We have also fixed code review permissions for partners so both
    parties can view a code review directly (the primary submitter no
    longer needs to share feedback with the partner).</p>

    <p>Finally, we've been a bit disorganized about recording
    extensions when students need to resubmit because they forgot to
    list their partner (or for other trivial reasons).  This is
    because I (Tyler) didn't provide TAs with good way to record
    extensions until recently, so everybody kept their own notes.  If
    you had an extension from a TA but you still see late days used
    below, please email me (tylerharter@gmail.com).  Be sure to tell
    me the following: (1) which project, (2) which TA granted the
    extension, and (3) how long the extension was.</p>

    <p>Your project summary (through P6) is below:</p>
    """

    html = intro.split('\n')
    for p in prows:
        html.append('<h2>' + p['project'].upper() + '</h2>')
        html.append('<ul>')
        line = '<li>Feedback: <a href="{}">{} reviewer comments</a>'
        html.append(line.format(p['code_review_url'], p['comment_count']))
        html.append('<li>Score: ' + str(p['score']))
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

    for net_id in net_ids:
        prows = projects[net_id]
        prows.sort(key=lambda row: int(row['project'][1:]))
        html = gen_html(prows)
        email = {'to':net_id+'@wisc.edu',
                 'subject': 'CS 301: Project Summary',
                 'message':html, 'html':True}
        emails.append(email)

    # dump email file
    with open('project_emails.json', 'w') as f:
        json.dump(emails, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
