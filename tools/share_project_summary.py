import os, sys, json, math
from collections import defaultdict as ddict

TEST_NET_IDS = None
TEST_NET_IDS = ['tharter']

def gen_html(prows):
    html = []
    for p in prows:
        html.append('<h2>' + p['project'].upper() + '</h2>')
        html.append('<ul>')
        html.append('<li>Feedback: <a href="{}">{} reviewer comments</a>'.format(p['code_review_url'], 'X'))
        html.append('<li>Score: ' + str(p['score']))
        html.append('<li>Days Late: ' + str(p['late_days']))
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

        print(html)

    # dump email file
    with open('project_emails.json', 'w') as f:
        json.dump(emails, f)

if __name__ == '__main__':
    main()
