msg = 'hello'


def greeting():
    print('greeting: ' + msg)
    msg = 'welcome!'


print('before: ' + msg)
greeting()
print('after: ' + msg)

# LESSON 7: assignment to a variable should be before its use in a
# function, even if there's a a global variable with the same name