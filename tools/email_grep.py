import os, sys, json

def main():
    if len(sys.argv) < 3:
        print('Usage: python email_grep.py <emails.json> <filter>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        emails = json.load(f)

    emails = [e for e in emails if e['message'].find(sys.argv[2]) >= 0]
    print('%d emails match' % len(emails))

    body = ""
    for i, email in enumerate(emails):
        if not email['message'].find(sys.argv[2]) >= 0:
            continue
        if i > 0:
            body += "<hr>\n"
        body += '<b>TO: </b> ' + email['to'] + '<br>'
        body += '<b>SUBJECT: </b> ' + email['subject'] + '<br>'
        body += email['message']

    html = """<html>
  <body>
    {body}
  </body>
</html>"""

    with open('out.html', 'w') as f:
        f.write(html.format(body=body))
    print('summary in out.html')

if __name__ == '__main__':
    main()
