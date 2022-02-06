x = 'A'

def f(x):
    x = 'B'
    print('inside: ' + x)

print('before: ' + x)
f(x)
print('after: ' + x)
