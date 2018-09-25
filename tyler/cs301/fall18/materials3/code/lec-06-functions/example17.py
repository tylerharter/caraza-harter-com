x = 'A'


def f(x):
    x = 'B'
    print('inside: ' + x)


print('before: ' + x)
f(x)
print('after: ' + x)

# LESSON 10: it's irrelevant whether the
# argument (outside) and parameter (inside)
# have the same variable name