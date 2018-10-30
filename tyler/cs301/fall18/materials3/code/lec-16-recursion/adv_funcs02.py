def call_it(my_function):
    print("calling", my_function)
    my_function()

def test():
    print("inside test function")

call_it(test)