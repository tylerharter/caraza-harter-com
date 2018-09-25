msg = 'hello'


def greeting():
    msg = 'welcome!'
    print('greeting: ' + msg)


print('before: ' + msg)
greeting()
print('after: ' + msg)

# LESSON 6: if you do an assignment to a variable
# in a function,Python assumes you want it local
