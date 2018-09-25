msg = 'hello'


def greeting():
    global msg
    print('greeting: ' + msg)
    msg = 'welcome!'


print('before: ' + msg)
greeting()
print('after: ' + msg)

# LESSON 8: use a global declaration to prevent Python from creating a
# local variable when you want a global variable
