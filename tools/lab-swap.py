import os, sys, csv, random, json
from collections import defaultdict as ddict

class Swapper:
    def __init__(self):
        times = set()
        with open('lab-swap (Responses) - Form Responses 1.csv') as f:
            reqs = {}
            for row in csv.DictReader(f):
                reqs[row['Email Address']] = dict(row)
            reqs = list(reqs.values())

        for req in reqs:
            req['from'] = req.pop('What is your current lab time?')
            req['to'] = req.pop('Which sections would you prefer?').split(', ')
            times.add(req['from'])
            for to in req['to']:
                times.add(to)

        self.times = times
        self.reqs = reqs

    def swap(self):
        swaps = []

        enrolled = {}
        enrolled['Thu @ 9:30am'] = 48
        enrolled['Thu @ 11am'] = 52
        enrolled['Thu @ 1pm'] = 52
        enrolled['Thu @ 2:30pm'] = 51
        enrolled['Thu @ 4pm'] = 50
        enrolled['Fri @ 9:30am'] = 49
        enrolled['Fri @ 11am'] = 48
        enrolled['Fri @ 1pm'] = 52
        enrolled['Fri @ 2:30pm'] = 39
        enrolled['Fri @ 4pm'] = 41

        with open('/Users/trh/git_co/cs301/s19/lab-swaps/lab-swap.json') as f:
            for row in json.load(f):
                if row.get("status", "") == "rejected":
                    continue
                enrolled[row["from"]] -= 1
                enrolled[row["to"]] += 1

        random.shuffle(self.reqs)
        for req in self.reqs:
            # find target with least enrollment
            dst = req['to'][0]
            for dst2 in req['to'][1:]:
                if enrolled[dst2] < enrolled[dst]:
                    dst = dst2

            if enrolled[dst] < 54:
                enrolled[dst] += 1
                enrolled[req['from']] -= 1
                swaps.append({
                    "email": req["Email Address"],
                    "from": req["from"],
                    "to": dst,
                })
            else:
                print('fail:', req["Email Address"], req["from"], req["to"])

        for time in sorted(enrolled.keys()):
            print(time, enrolled[time])

        return swaps


def main():
    s = Swapper()
    swaps = s.swap()
    with open('lab-swap.json', 'w') as f:
        json.dump(swaps, f, indent=2, sort_keys=True)

    emails = []
    for swap in swaps:
        message = """
Hello, as per your request, we have moved you from the {} lab to the {} lab.  This is an informal change (it won't be reflected in student center).  We have informally moved other students as well, so please contact Tyler at tylerharter@gmail.com if you change your mind and prefer your original time instead (we need to be careful not to overcrowd any one lab).
""".strip().format(swap["from"], swap["to"])
        email = {
            "to": swap["email"],
            "subject": "CS 301 - Lab Section Swap",
            "message": message
        }
        emails.append(email)
    with open('emails.json', 'w') as f:
        json.dump(emails, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
