import os, sys, json, copy

COURSE = 'a'
not_reviewed = {'p1'}
CR_URL = 'https://tyler.caraza-harter.com/cs301/fall19/code_review.html?project_id=%s&student_email=%s@wisc.edu'

def try_read_json(path, default={}):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return copy.deepcopy(default)


class Grades:
    def __init__(self, project):
        self.project = project
        with open('roster.json') as f:
            net_ids = {row['net_id'] for row in json.load(f) if row['enrolled']}

        self.grade_rows = [self.get_grade_row(nid) for nid in net_ids]


    def dump(self, path):
        with open(path, "w") as f:
            f.write('[\n')
            for i, row in enumerate(self.grade_rows):
                json.dump(row, f)
                if i < len(self.grade_rows) - 1:
                    f.write(",")
                f.write("\n")
            f.write(']\n')


    def get_grade_row(self, net_id):
        dirname = 'snapshot/%s/projects/%s/%s*at*wisc.edu' % (COURSE, self.project, net_id)
        link = None
        if os.path.exists(dirname):
            links = [p for p in os.listdir(dirname) if p.endswith('-link.json')]
            if len(links) > 0:
                link = max(links)
                with open(os.path.join(dirname, link)) as f:
                    link = json.load(f)['symlink']

        # we need to check four files:
        # - tests
        # - CR
        # - submission (to determine lateness)
        # - extensions (to adjust lateness)

        ready = False
        if link:
            sub = try_read_json(os.path.join("snapshot", COURSE, link, "submission.json"), {})
            test = try_read_json(os.path.join("snapshot", COURSE, link, "test.json"), {})
            cr = try_read_json(os.path.join("snapshot", COURSE, link, "cr.json"), {})
            if sub != {} and test != {} and (cr != {} or self.project in not_reviewed):
                test_score = test.get("score", 0)
                ta_deduction = cr.get("points_deducted", 0)
                late_days = max(sub.get("late_days", 0), 0)
                # late_days -=    TODO: record extensions!
                ready = True

        if not ready:
            test_score = 0
            ta_deduction = 0
            late_days = 0

        score = max(test_score - ta_deduction, 0)
        cr_url = CR_URL % (self.project, net_id)

        return {"project": self.project, "net_id": net_id, "test_score": test_score,
                "ta_deduction": ta_deduction, "score": score, "late_days": late_days,
                "code_review_url": cr_url}


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_grades.py p1 [p2 ...]")
    for project in sys.argv[1:]:
        Grades(project).dump(os.path.join('grades', project+'.json'))


if __name__ == '__main__':
     main()
