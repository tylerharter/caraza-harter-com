import math


def f(x):
    y = 2 * math.e ** x + 3 * x ** 3 - 1
    return y


def volume_of_cylinder(radius, height=1):
    volume = math.pi * radius * radius * height
    return volume


out1 = f(1)
print('f(x) =', out1)

v = volume_of_cylinder(5, 10)
print('volume =', v)

# height will the default value (i.e., 1)
v = volume_of_cylinder(5)
print('volume =', v)
