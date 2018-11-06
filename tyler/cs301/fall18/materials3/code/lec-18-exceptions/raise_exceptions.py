import math


def area(r):
    if type(r) not in (int, float):
        raise TypeError("radius should be an int or float")
    return math.pi * r ** 2


try:
    print(area("10"))
except Exception as e:
    print("Exception:", str(e))


print("Program exited gracefully!")
