def f(x):
    x = 'B'
    print('inside: ' + x)


val = 'A'
print('before: ' + val)
f(val)
print('after: ' + val)

# LESSON 9: in Python, arguments are "passed by value", meaning changes
# to a parameter inside the function don't change the argument outside