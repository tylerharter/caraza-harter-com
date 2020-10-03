def f(*args, **kwargs):
    print("ARGS", args)
    print("KWARGS", kwargs)

f(1, 2, x=3, y=4, z=5)
