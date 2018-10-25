from pprint import pprint

person = dict()
person['name'] = 'Mike Swift'
person['age'] = 37
person['isAlive'] = True
person['phone'] = [{'type': 'office', 'number': '608-123-4567'},
                   {'type': 'home', 'number': '608-987-6543'}]
person['address'] = {'street': '1210 West Dayton Street',
                     'city': 'Madison',
                     'state': 'WI',
                     'zip': 53706}
# pretty print
pprint(person)
