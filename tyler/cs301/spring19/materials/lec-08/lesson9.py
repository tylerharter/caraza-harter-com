def f(x):
    x = 'B'
    print('inside: ' + x)

val = 'A'
print('before: ' + val)
f(val)
print('after: ' + val)
