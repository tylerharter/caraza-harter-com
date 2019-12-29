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

    temp = pd.read_csv("~/g/cs301/f19/grades/canvas-v35.csv")
    temp["email"] = temp["SIS Login ID"].str.lower()
    temp.set_index("email", inplace=True)
    canvas = pd.DataFrame()
    for col in temp.columns:
        m = re.match(r'(P\d+) \(', col)
        if m:
            canvas[m.group(1).lower()] = 100.0 * temp[col] / temp[col].iloc[0]

    summaries = {}
            
    with open(path) as f:
        for row in csv.DictReader(f):
            email = row["Email Address"]
            partner = row["If you have a partner who was also affected, you can fill their wiscmail (netid@wisc.edu) address here so they don't need to submit a separate form."]
            proj = row["Which Project?"].lower()
            expected = row['What score (out of 100) do you think you should get?']
            actual = canvas.loc[email, proj]

            partner = partner.strip().lower()
            if partner:
                if not partner.endswith("@wisc.edu"):
                    partner += "@wisc.edu"
                partner_actual = canvas.loc[partner, proj]
                assert actual == partner_actual

            s3_path = '%s/extensions/%s/%s.json' % (COURSE, proj, email.replace("@", "*at*"))
            body = {"approver":"script", "days":days}
            body = bytes(json.dumps(body), 'utf-8')
            #s3.put_object(Bucket=BUCKET, Key=s3_path, Body=body, ContentType='text/plain')

            url = 'https://tyler.caraza-harter.com/cs301/fall19/code_review.html?project_id={}&student_email={}'
            url = url.format(proj, email)
            if float(expected) > actual:
                html.append('<a href="%s">%s %s (expected=%s, actual=%d)</a><br>'
                            % (url, proj, email.replace("*at*", "@"), expected, actual))

                url = 'https://tyler.caraza-harter.com/cs301/fall19/messages.html?topic=projects&student_email=%s' % email
                summaries[email] = ('<a href="%s">%s</a><br>' % (url, email.replace("*at*", "@")))

    print("issues:", len(html))

    html = ["<h1>Issues</h1>"] + sorted(html)
    html.extend(["<h1>People</h1>"] + sorted(summaries.values()))

    with open("issues.html", "w") as f:
        f.write("\n".join(html))
    print("people:", len(summaries))

if __name__ == '__main__':
    main()
