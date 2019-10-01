import os, sys, json, copy
from collections import defaultdict as ddict

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

        self.extensions = self.get_extensions()
        self.grade_rows = [self.get_student_grade(nid) for nid in net_ids]


    # returns dict
    # key: submission file path
    # val: days extended
    def get_extensions(self):
        extensions = ddict(int)
        
        dirname = 'snapshot/%s/extensions/%s/' % (COURSE, self.project)
        for name in os.listdir(dirname):
            if not name.endswith(".json"):
                continue
            path = os.path.join(dirname, name)
            with open(path) as f:
                days = json.load(f)["days"]
            net_id = name.split("*at*")[0]
            links = self.get_proj_links(net_id)
            for link in links:
                with open(link) as f:
                    sub = json.load(f)['symlink']
                    extensions[sub] = max(extensions[sub], days)
        return extensions


    def dump(self, path):
        with open(path, "w") as f:
            f.write('[\n')
            for i, row in enumerate(self.grade_rows):
                json.dump(row, f)
                if i < len(self.grade_rows) - 1:
                    f.write(",")
                f.write("\n")
            f.write(']\n')


    def get_proj_links(self, net_id):
        dirname = 'snapshot/%s/projects/%s/%s*at*wisc.edu' % (COURSE, self.project, net_id)
        link = None
        if os.path.exists(dirname):
            return [os.path.join(dirname, p) for p in os.listdir(dirname) if p.endswith('-link.json')]
        return []


    def get_student_grade(self, net_id):
        grade = self.get_submission_grade(net_id, None)
        links = sorted(self.get_proj_links(net_id))
        for link in links:
            with open(link) as f:
                submission_dir = json.load(f)['symlink']
            grade2 = self.get_submission_grade(net_id, submission_dir)
            # only take a later submission over a prior one if the
            # score is better, because the earlier one will incur
            # fewer late days
            if grade2["score"] > grade["score"]:
                grade = grade2
        else:
            submission_dir = None

        return grade


    def get_submission_grade(self, net_id, submission_dir):
        # we need to check four files:
        # - tests
        # - CR
        # - submission (to determine lateness)
        # - extensions (to adjust lateness)

        ready = False
        if submission_dir:
            sub = try_read_json(os.path.join("snapshot", COURSE, submission_dir, "submission.json"), {})
            test = try_read_json(os.path.join("snapshot", COURSE, submission_dir, "test.json"), {})
            cr = try_read_json(os.path.join("snapshot", COURSE, submission_dir, "cr.json"), {})
            if sub != {} and test != {} and (cr != {} or self.project in not_reviewed):
                test_score = test.get("score", 0)
                ta_deduction = cr.get("points_deducted", 0)
                late_days = max(sub.get("late_days", 0) - self.extensions[submission_dir], 0)
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
