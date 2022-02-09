msg = 'hello'

def greeting():
    print('greeting: ' + msg)
    msg = 'welcome!'

print('before: ' + msg)
greeting()
print('after: ' + msg)
