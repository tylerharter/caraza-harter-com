import os, sys, json

def try_read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.loads(f.read())

class Snapshot:
    def __init__(self, dirname):
        self.dirname = dirname
        with open(dirname + '/users/roster.json') as f:
            roster = json.loads(f.read())
            self.roster = [row for row in roster if 'net_id' in row]

    def net_id_to_google_id(self, net_id):
        path = self.dirname+'/users/net_id_to_google/%s.txt' % net_id
        if not os.path.exists(path):
            return {}
        with open(path) as f:
            return f.read()

    def project_submission(self, project_id, net_id):
        """get submission code and metadata"""
        google_id = self.net_id_to_google_id(net_id)
        if not google_id:
            return {}
        path = self.dirname+'/projects/'+project_id+'/users/'+google_id+'/curr.json'
        return try_read_json(path)

    def test_result(self, project_id, net_id):
        """get auto grade for submission"""
        path = self.dirname+'/ta/grading/'+project_id+'/'+net_id+'.json'
        return try_read_json(path)

    def submission_details(self, project_id, net_id):
        return {
            'submission': self.project_submission(project_id, net_id),
            'test':       self.test_result(project_id, net_id),
            'cr':         None
        }

    def project_csv(self, project_id):
        net_ids = set(student['net_id'] for student in self.roster)
        rows = {}

        def add_row(net_id, score, submitter):
            # many students could specify the same student as their partner.
            # we tally this up to identify this problem
            submissions = 1
            row = {
                'net_id': net_id,
                TEST_SCORE,
                TA_DEDUCTION,
                LATE_DAYS,
                'score': score,
                'primary': submitter,
                'partner': '',
                'submissions': 1,
            }
            rows[net_id] = row

        # PASS 1: students who were primary submitter
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            score = details.get('test', {}).get('score', None)
            net_id = student['net_id']
            if score == None:
                continue

            add_row(net_id, score, submitter=True)

        # PASS 2: students with a partner who submitted
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            score = details.get('test', {}).get('score', None)
            net_id = details.get('submission', {}).get('partner_netid', None)
            if score == None or net_id == None or not net_id in net_ids:
                continue
            if net_id in rows:
                rows[net_id]['submissions'] += 1

            add_row(net_id, score, submitter=False)

            # associate students with each other
            rows[net_id]['partner'] = student['net_id']
            rows[student['net_id']]['partner'] = net_id

        # PASS 3: students who did not submit
        for student in self.roster:
            net_id = student['net_id']
            if not net_id in rows:
                add_row(net_id, 0, submitter=False)

        for row in rows.values():
            print(row)

def main():
    if len(sys.argv) < 3:
        print('Usage: python project_summary.py <snap-dir> <project_id1> [<project_id2> ...]')
        sys.exit(1)
    snap_dir = sys.argv[1]
    snap = Snapshot(snap_dir)
    for project_id in sys.argv[2:]:
        snap.project_csv(project_id)

if __name__ == '__main__':
    main()
