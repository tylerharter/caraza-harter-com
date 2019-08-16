import os, sys, json, re
from project_summary import Snapshot

def main():
    net_ids = []
    for p in ['p7', 'p8', 'p9']:
        for user in os.listdir('snapshot/projects/'+p+'/users/'):
            dirname = 'snapshot/projects/'+p+'/users/'+user
            for name in os.listdir(dirname):
                m = re.match(r'rating-(.*?)-\d+\.\d+\.json', name)
                if m:
                    net_id = m.group(1)
                    path = dirname+'/'+name
                    net_ids.append(net_id)
    with open("raters.json", "w") as f:
        json.dump(sorted(set(net_ids)), f)
                    

if __name__ == '__main__':
     main()
