import math

def is_close(val1, val2):
    diff = abs(val1 - val2)
    return diff < 0.0001 or diff / max(abs(val1), abs(val2)) < 0.01

def is_approx_pi(value):
    return is_close(value, math.pi)

def is_approx_zero(value):
    return is_close(value, 0)

x = input("please enter a number: ")
x = float(x)
print("your x is: ", x)
print("close to pi?", is_approx_pi(x))
print("close to zero?", is_approx_zero(x))
