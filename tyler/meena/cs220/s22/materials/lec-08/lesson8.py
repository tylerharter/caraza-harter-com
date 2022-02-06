msg = 'hello'

def greeting():
    global msg
    print('greeting: ' + msg)
    msg = 'welcome!'

print('before: ' + msg)
greeting()
print('after: ' + msg)
