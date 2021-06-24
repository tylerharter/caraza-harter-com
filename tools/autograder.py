import os, sys, json, base64
from subprocess import check_output, CalledProcessError, STDOUT
import boto3

# this only works for the 220 online format

BUCKET = 'caraza-harter-cs301'
COURSE = "c"

# submission.json => pN.ipynb (both inside snapshot subdir)
def extract(submit_path):
    with open(submit_path) as f:
        sub = json.load(f)
    dirname = os.path.dirname(submit_path)
    filename = sub["filename"]
    payload = base64.b64decode(sub["payload"])
    outpath = os.path.join(dirname, filename)
    with open(outpath, "wb") as f:
        f.write(payload)
    return outpath

# AWS profile for boto3
def get_profile_name():
    if not os.path.exists("aws_profile.txt"):
        profile = input("What is the name of your AWS profile in the credentials file? ")
        with open("aws_profile.txt", "w") as f:
            f.write(profile)
    with open("aws_profile.txt") as f:
        profile = f.read().strip()
    print(f"using profile {profile} from aws_profile.txt")
    return profile

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 autograder.py (grade|upload) pN")
        return

    session = boto3.Session(profile_name=get_profile_name())
    s3 = session.client('s3')

    op = sys.argv[1]
    project = sys.argv[2]
    dirname = os.path.join("snapshot", COURSE, "projects", project)
    submission_dirs = []
    for root, _, files in os.walk(dirname):
        for fn in files:
            if fn == "submission.json":
                submission_dirs.append(root)
                break

    for sdir in submission_dirs:
        spath = os.path.join(sdir, "submission.json")
        ipynb = extract(spath)
        results = os.path.join(sdir, "test.json")

        if op == "grade":
            try:
                cmd = ["python3", "tester.py", ipynb, f"{project}-key.csv"]
                print(" ".join(cmd))
                out = check_output(cmd, stderr=STDOUT)
            except CalledProcessError as e:
                with open(results, "w") as f:
                    json.dump({"score": 0, "errors": [str(e.output)]}, f, indent=True)
            with open(results) as f:
                r = json.load(f)
                score = r["score"]
            print("SCORE", score, "\n")
        elif op == "upload":
            s3_path = "/".join(results.split(os.path.sep)[1:])
            print(s3_path)
            with open(results, "rb") as f:
                s3.put_object(Bucket=BUCKET, Key=s3_path, Body=f)
        else:
            raise Exception(f"bad op: {op}")

if __name__ == '__main__':
     main()
