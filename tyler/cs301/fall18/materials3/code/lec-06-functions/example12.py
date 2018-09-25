# show global frame in PythonTutor

msg = 'hello'   # global, because outside any function


def greeting():
    print(msg)


print('before: ' + msg)
greeting()
print('after: ' + msg)

# LESSON 5: you can generally just use
# global variables inside a function
