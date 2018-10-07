import os, sys, json, math

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

    def project_code_review(self, project_id, net_id):
        """get code review for project"""
        google_id = self.net_id_to_google_id(net_id)
        if not google_id:
            return {}
        path = self.dirname+'/projects/'+project_id+'/users/'+google_id+'/cr.json'
        return try_read_json(path)
    
    def test_result(self, project_id, net_id):
        """get auto grade for submission"""
        path = self.dirname+'/ta/grading/'+project_id+'/'+net_id+'.json'
        return try_read_json(path)

    def submission_details(self, project_id, net_id):
        return {
            'submission': self.project_submission(project_id, net_id),
            'cr':         self.project_code_review(project_id, net_id),
            'test':       self.test_result(project_id, net_id),
        }

    def project_json(self, project_id, out_path):
        net_ids = set(student['net_id'] for student in self.roster)
        rows = {}

        def add_row(net_id, filename, test_score, ta_deduction, late_days, submitter):
            score = max(test_score - ta_deduction, 0)
            
            # many students could specify the same student as their partner.
            # we tally this up to identify this problem
            submissions = 1

            row = {
                'project': project_id,
                'net_id': net_id,
                'primary': submitter,
                'partner': None,
                'filename': filename,
                'submissions': 1,
                'test_score': test_score,
                'ta_deduction': ta_deduction,
                'score': score,
                'late_days': late_days,
            }
            rows[net_id] = row

        # PASS 1: students who were primary submitter
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            test_score = details.get('test', {}).get('score', None)
            ta_deduction = details.get('cr', {}).get('points_deducted', 0)
            late_days = max(math.ceil(details.get('submission', {}).get('late_days', 0)), 0)
            filename = details.get('submission', {}).get('filename', None)
            net_id = student['net_id']
            if test_score == None:
                continue

            add_row(net_id, filename, test_score, ta_deduction, late_days, submitter=True)

        # PASS 2: students with a partner who submitted
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            test_score = details.get('test', {}).get('score', None)
            ta_deduction = details.get('cr', {}).get('points_deducted', 0)
            late_days = max(math.ceil(details.get('submission', {}).get('late_days', 0)), 0)
            filename = details.get('submission', {}).get('filename', None)
            net_id = details.get('submission', {}).get('partner_netid', None)
            if test_score == None or net_id == None or not net_id in net_ids:
                continue
            if net_id in rows:
                rows[net_id]['submissions'] += 1

            add_row(net_id, filename, test_score, ta_deduction, late_days, submitter=False)

            # associate students with each other
            rows[net_id]['partner'] = student['net_id']
            rows[student['net_id']]['partner'] = net_id

        # PASS 3: students who did not submit
        for student in self.roster:
            net_id = student['net_id']
            if not net_id in rows:
                add_row(net_id, None, 0, 0, late_days, submitter=False)

        output = ('[\n' +
                  ',\n'.join([json.dumps(row) for row in rows.values()]) +
                  ']\n')
        with open(out_path, 'w') as f:
            f.write(output)

def main():
    if len(sys.argv) < 3:
        print('Usage: python project_summary.py <snap-dir> <project_id1> [<project_id2> ...]')
        sys.exit(1)
    snap_dir = sys.argv[1]
    snap = Snapshot(snap_dir)

    if not os.path.exists('./grades'):
        os.makedirs('./grades')
    for project_id in sys.argv[2:]:
        snap.project_json(project_id, 'grades/'+project_id+'.json')

if __name__ == '__main__':
    main()
