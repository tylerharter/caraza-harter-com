import os, sys, requests, json

mailgun_key = None
def mgkey():
    global mailgun_key
    if mailgun_key == None:
        with open(os.path.expanduser('~/.cred/mailgun.txt')) as f:
            mailgun_key = f.read().strip()
    return mailgun_key

def send_mail(to, subject, message, use_html):
    data = {"from": "CS 301 <no-reply@caraza-harter.com>",
            "to": [to],
            "subject": subject}
    if use_html:
        data['html'] = message
    else:
        data['text'] = message

    return requests.post(
        "https://api.mailgun.net/v3/caraza-harter.com/messages",
        auth=("api", mgkey()),
        data=data)

def main():
    if len(sys.argv) != 2:
        print('Usage: python email_announcement.py emails.json')
        return

    path = sys.argv[1]
    with open(path) as f:
        rows = json.loads(f.read())

    while len(rows) > 0:
        row = rows.pop()
        print("send to " + row['to'])
        resp = send_mail(to=row['to'], subject=row['subject'],
                         message=row['message'], use_html=row.get('html', False))
        assert(resp.status_code == 200)
        with open(path, 'w') as f:
            f.write(json.dumps(rows, indent=2))

if __name__ == '__main__':
    main()
