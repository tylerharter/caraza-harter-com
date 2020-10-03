def trace(fn):
    def wrap(*args, **kwargs):
        print("CALL {}(*{}, **{})".format(fn.__name__, args, kwargs))
        return fn(*args, **kwargs)
    return wrap

@trace
def add(x, y):
    return x+y

@trace
def mult(x, y):
    return x*y

print(add(1, 2))
print(add(x=1, y=2))
print(mult(2, y=3))
