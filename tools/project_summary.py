import os, sys, json, math, datetime

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
            self.roster = [row for row in roster]


    def net_id_to_google_id(self, net_id):
        path = self.dirname+'/users/net_id_to_google/%s.txt' % net_id
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return f.read()


    def code_review_url(self, submitter_net_id, project_id):
        submitter_user_id = self.net_id_to_google_id(submitter_net_id)
        if submitter_user_id == None:
            return None
        url = 'https://tyler.caraza-harter.com/cs301/fall18/code_review.html?'
        url += 'project_id=' + project_id
        url += '&submitter_id=' + submitter_user_id
        return url


    def project_submission(self, project_id, net_id):
        """get submission code and metadata"""
        google_id = self.net_id_to_google_id(net_id)
        if not google_id:
            return {}
        path = self.dirname+'/projects/'+project_id+'/users/'+google_id+'/curr.json'
        return try_read_json(path)


    def project_extension(self, project_id, net_id):
        """get submission extension details"""
        google_id = self.net_id_to_google_id(net_id)
        if not google_id:
            return {}
        path = self.dirname+'/projects/'+project_id+'/users/'+google_id+'/extension.json'
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
            'extension':  self.project_extension(project_id, net_id),
            'cr':         self.project_code_review(project_id, net_id),
            'test':       self.test_result(project_id, net_id),
        }


    def get_comment_count(self, cr):
        count = 0
        if not cr.get('general_comments', '') in (None, ''):
            count += 1
        highlights = cr.get('highlights', {})
        for filename in highlights:
            count += len(highlights[filename])
        return count


    def project_json(self, project_id, out_path):
        net_ids = set(student['net_id'] for student in self.roster)

        # key: net_id
        # val: submission details
        rows = {}

        def add_row(net_id, filename, test_score, ta_deduction, late_days, comment_count, submitter):
            score = max(test_score - ta_deduction, 0)

            # TODO: in spring semester of 2018, start counting late days for first three projects
            # we decided not to count these late this semester because there were too many
            # resubmissions
            if project_id in ('p1','p2','p3'):
                late_days = 0
            assert(datetime.datetime.now().year == 2018)

            # many students could specify the same student as their partner.
            # we tally this up to identify this problem
            submissions = 1

            row = {
                'project': project_id,
                'net_id': net_id,
                'user_id': self.net_id_to_google_id(net_id),
                'primary': submitter,
                'partner': None, # set later
                'filename': filename,
                'submissions': 1,
                'test_score': test_score,
                'ta_deduction': ta_deduction,
                'score': score,
                'late_days': late_days,
                'comment_count': comment_count
            }
            rows[net_id] = row

        # PASS 1: students who were primary submitter
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            test_score = details.get('test', {}).get('score', None)
            ta_deduction = details.get('cr', {}).get('points_deducted', 0)

            late_days = details.get('submission', {}).get('late_days', 0)
            late_days -= details.get('extension', {}).get('days', 0)
            late_days = max(math.ceil(late_days), 0)

            comment_count = self.get_comment_count(details.get('cr', {}))
            filename = details.get('submission', {}).get('filename', None)
            net_id = student['net_id']
            if test_score == None:
                continue

            add_row(net_id, filename, test_score, ta_deduction,
                    late_days, comment_count, submitter=True)

        # PASS 2: students with a partner who submitted
        for student in self.roster:
            details = self.submission_details(project_id, student['net_id'])
            test_score = details.get('test', {}).get('score', None)
            ta_deduction = details.get('cr', {}).get('points_deducted', 0)

            late_days = details.get('submission', {}).get('late_days', 0)
            late_days -= details.get('extension', {}).get('days', 0)
            late_days = max(math.ceil(late_days), 0)

            comment_count = self.get_comment_count(details.get('cr', {}))
            filename = details.get('submission', {}).get('filename', None)
            net_id = details.get('submission', {}).get('partner_netid', None)
            if test_score == None or net_id == None or not net_id in net_ids:
                continue
            if net_id in rows:
                rows[net_id]['submissions'] += 1

            add_row(net_id, filename, test_score, ta_deduction,
                    late_days, comment_count, submitter=False)

            # associate students with each other
            rows[net_id]['partner'] = student['net_id']
            rows[student['net_id']]['partner'] = net_id

        # PASS 3: students who did not submit
        for student in self.roster:
            net_id = student['net_id']
            if not net_id in rows:
                add_row(net_id, None, 0, 0,
                        late_days, 0, submitter=False)

        # add code review URLs for every row
        for row in rows.values():
            if row["primary"] or row["filename"] == None:
                url = self.code_review_url(row['net_id'], row['project'])
            else:
                url = self.code_review_url(row['partner'], row['project'])
            row['code_review_url'] = url

        # filter out students who have dropped.
        # we do this last because students who dropped may have a partner still enrolled
        enrolled_net_ids = set(student['net_id'] for student
                               in self.roster
                               if student.get('enrolled', True))
        to_drop = net_ids - enrolled_net_ids
        for net_id in to_drop:
            rows.pop(net_id)

        # save output
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
