msg = 'hello' # global, outside any func

def greeting():
    print(msg)

print('before: ' + msg)
greeting()
print('after: ' + msg)
