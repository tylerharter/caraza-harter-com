import boto3, botocore, base64, json, os, sys, csv, re
from multiprocessing import Pool
import pandas as pd

BUCKET = 'caraza-harter-cs301'
COURSE = 'a'

def main():
    session = boto3.Session()
    s3 = session.client('s3')
    if len(sys.argv) < 2:
        print("Usage: python mass_extensions.py <requests.csv> [<days>]")
        return

    path = sys.argv[1]
    if len(sys.argv) >= 3:
        days = int(sys.argv[2])
    else:
        days = 999
    html = []

    temp = pd.read_csv("~/g/cs301/f19/grades/canvas-v25.csv")
    temp["email"] = temp["SIS Login ID"].str.lower()
    temp.set_index("email", inplace=True)
    canvas = pd.DataFrame()
    for col in temp.columns:
        m = re.match(r'(P\d+) \(', col)
        if m:
            canvas[m.group(1).lower()] = 100.0 * temp[col] / temp[col].iloc[0]

    with open(path) as f:
        for row in csv.DictReader(f):
            email = row["Email Address"]
            proj = row["Which Project?"].lower()
            expected = row['What score (out of 100) do you think you should get?']
            actual = canvas.loc[email, proj]
            s3_path = '%s/extensions/%s/%s.json' % (COURSE, proj, email.replace("@", "*at*"))
            body = {"approver":"script", "days":days}
            body = bytes(json.dumps(body), 'utf-8')
            s3.put_object(Bucket=BUCKET, Key=s3_path, Body=body, ContentType='text/plain')
            print(s3_path)

            url = 'https://tyler.caraza-harter.com/cs301/fall19/code_review.html?project_id={}&student_email={}'
            url = url.format(proj, email)

            if not re.match(r'\d+(\.\d+)?', expected) or float(expected) > actual:
                html.append('<a href="%s">%s %s (expected=%s, actual=%d)</a><br>'
                            % (url, proj, email.replace("*at*", "@"), expected, actual))
            print(url)

    with open("issues.html", "w") as f:
        f.write("\n".join(sorted(html)))
    print("lines:", len(html))

if __name__ == '__main__':
    main()
