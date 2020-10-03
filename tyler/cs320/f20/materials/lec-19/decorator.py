def function_A():
    print("A")

def decorate(fn):
    print("decorating!")
    return function_A

@decorate
def function_B():
    print("B")

function_B() # prints "A"!
