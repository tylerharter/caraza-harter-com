import os, sys, json, random
from collections import defaultdict as ddict

# upload with something like this:
#
# aws s3 cp p2-cr-assignments.json s3://caraza-harter-cs301/a/projects/p2-cr-assignments.json

COURSE = 'a'
PROJECT = 'p4'

# we want submissions that are the latest for a student
def get_submission_emails():
    # key is user email
    links = ddict(list)
    submissions = ddict(list)

    for d, _, file_paths in os.walk('snapshot/%s/projects/%s' % (COURSE, PROJECT)):
        for path in file_paths:
            path = os.path.join(d, path)
            email = path.split(os.sep)[4].replace('*at*', '@')
            if path.endswith('-link.json'):
                links[email].append(path)
            elif path.endswith('submission.json'):
                submissions[email].append(path)

    for email, values in links.items():
        latest = sorted(values)[-1]
        sub = latest.replace('-link.json', os.sep+'submission.json')
        if sub in submissions[email]:
            yield email


def main():
    submitters = sorted(get_submission_emails())
    with open('roster.json') as f:
        emails = {row['net_id']+'@wisc.edu' for row in json.load(f) if row['enrolled']}
    submitters = emails & set(submitters)
    others = emails - set(submitters)
    # put people who actually submitted first so we balance better
    students = sorted(submitters) + sorted(others)

    tas = []
    with open("tas.json") as f:
        for row in json.load(f):
            tas.extend([row['name']] * row['weight'])
    random.shuffle(tas)

    assignments = {}
    for i, student in enumerate(students):
        assignments[student] = tas[i % len(tas)]
    with open('%s-cr-assignments.json' % PROJECT, 'w') as f:
        json.dump(assignments, f, indent=2)


if __name__ == '__main__':
     main()
