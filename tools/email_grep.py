import os, sys, json

def main():
    if len(sys.argv) < 3:
        print('Usage: python email_grep.py <emails.json> <filter>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        emails = json.load(f)

    body = ""
    count = 0
    for i, email in enumerate(emails):
        if email['message'].find(sys.argv[2]) == -1 and email['to'].find(sys.argv[2]) == -1:
            continue
        if i > 0:
            body += "<hr>\n"
        body += '<b>TO: </b> ' + email['to'] + '<br>'
        body += '<b>SUBJECT: </b> ' + email['subject'] + '<br>'
        body += email['message']
        count += 1
    html = """<html>
  <body>
    {body}
  </body>
</html>"""

    print(count, "matches")

    with open('out.html', 'w') as f:
        f.write(html.format(body=body))
    print('summary in out.html')

if __name__ == '__main__':
    main()
