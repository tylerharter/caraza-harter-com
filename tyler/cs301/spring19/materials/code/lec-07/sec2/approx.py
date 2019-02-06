import math

def is_close(val1, val2):
    err = abs(val1 - val2)
    #return err / max(abs(val1), abs(val2)) < 0.01 or err < 0.00001
    return err < 0.00001 or err / max(abs(val1), abs(val2)) < 0.01

def is_approx_pi(x):
    return is_close(x, math.pi)

def is_approx_zero(x):
    return is_close(x, 0)

x = input("enter a number: ")
x = float(x)
print("x:", x)

print("is about pi?", is_approx_pi(x))
print("is about zero?", is_approx_zero(x))
