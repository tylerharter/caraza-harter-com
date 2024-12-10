import os, sys, json, math, datetime, boto3
from collections import defaultdict as ddict

COURSE = 'b'
BUCKET = 'caraza-harter-cs301'
s3 = boto3.client('s3')

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 secure_email.py <emails.json> <topic>")
        return

    filename, topic = sys.argv[1:]

    # can be a dict (email => message) or a list of dicts with more info per message
    with open(filename) as f:
        emails = json.load(f)

    for email in emails:
        if isinstance(email, str):
            email = {"to": email, "message": emails[email], "html": True, "subject": ""}

        print(email)
        assert(email['html'])

        path = '%s/messages/%s/%s.json' % (COURSE, email["to"].replace("@", "*at*").lower(), topic)
        print(path)
        s3.put_object(Bucket=BUCKET,
                      Key=path,
                      Body=bytes(json.dumps({'subject': email['subject'], 'msg': email['message']}), 'utf-8'),
                      ContentType='text/json')


if __name__ == '__main__':
    main()
