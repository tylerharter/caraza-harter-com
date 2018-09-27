def absolute_A(x):
    return (x ** 2) ** 0.5

def absolute_B(x):
    if x < 0:
        x = -x
    return x

def absolute_C(x):
    if x < 0:
        return -x
    else:
        return x

def absolute_D(x):
    if x < 0:
        return -x
    return x
