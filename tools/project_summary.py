import os, sys, json

class Snapshot:
    def __init__(self, dirname):
        self.dirname = dirname
        with open(dirname + '/users/roster.json') as f:
            self.roster = json.loads(f.read())

    def test_result(self, project_id, net_id):
        path = self.dirname+'/ta/grading/'+project_id+'/'+net_id+'.json'
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.loads(f.read())
            
    def project_csv(self, project_id):
        rows = []
        for student in self.roster:
            if not 'net_id' in student:
                continue
            net_id = student['net_id']
            row = {}
            row['net_id'] = net_id
            test_grade = self.test_result(project_id, net_id)
            row['score'] = test_grade.get('score', 0) if test_grade else 0
            print(row)
            rows.append(row)
            
def main():
    snap = Snapshot('snapshot')
    snap.project_csv('p1')

if __name__ == '__main__':
    main()
