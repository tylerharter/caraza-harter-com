def double(x):
    return 2 * x

def apply_f(f, items):
    for item in items:
        yield f(item)

for val in apply_f(double, [1,2,3]):
    print(val)
