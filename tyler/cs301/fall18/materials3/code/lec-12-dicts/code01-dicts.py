d = dict()

print(d)

d['one'] = 1
d['two'] = 2
d['three'] = 3


print(d)

# d2 = {1: 'one', 2: 'two', 3:'three'}
# print(d2)

for k in d:
    print(k, ":", d[k])

d['one'] = 4
print(d)