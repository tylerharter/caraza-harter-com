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
        diff = ddict(int)
        swaps = []

        diff['Thu @ 9:30am'] = -1
        diff['Thu @ 11am'] = 2
        diff['Thu @ 1pm'] = 3
        diff['Thu @ 2:30pm'] = 0
        diff['Thu @ 4pm'] = 0
        
        diff['Fri @ 9:30am'] = -1
        diff['Fri @ 11am'] = 1
        diff['Fri @ 1pm'] = 1
        diff['Fri @ 2:30pm'] = -12
        diff['Fri @ 4pm'] = -7

        random.shuffle(self.reqs)
        for req in self.reqs:
            # find target with least enrollment
            dst = req['to'][0]
            for dst2 in req['to'][1:]:
                if diff[dst2] < diff[dst]:
                    dst = dst2

            if diff[dst] < 4:
                diff[dst] += 1
                diff[req['from']] -= 1
                swaps.append({
                    "email": req["Email Address"],
                    "from": req["from"],
                    "to": dst,
                })
            else:
                print('fail:', req["Email Address"], req["from"], req["to"])

        for time in sorted(diff.keys()):
            print(time, diff[time])

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
