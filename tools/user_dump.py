import os, sys, json, base64
from project_summary import Snapshot

def main():
    if len(sys.argv) < 3:
        print('Usage: python project_summary.py <snap-dir> <net_id>')
        sys.exit(1)

    snap_dir = sys.argv[1]
    snap = Snapshot(snap_dir)
    net_id = sys.argv[2]

    for i in range(11):
        proj_id = 'p%d'%i
        proj = snap.project_submission(proj_id, net_id)
        if proj == None:
            print("SKIP", proj_id)
            continue
        filename = proj['filename']
        contents = base64.b64decode(proj['payload'])
        path = os.path.join(net_id, proj_id, filename)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, "wb") as f:
            f.write(contents)


if __name__ == '__main__':
     main()
