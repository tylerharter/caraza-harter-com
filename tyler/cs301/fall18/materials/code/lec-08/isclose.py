def isclose(a, b, tolerance=0.01):
    diff = abs(a-b)
    baseline = min(abs(a), abs(b))
    is_it = (baseline != 0) and (diff / baseline < tolerance)
    #is_it = (diff / baseline < tolerance) and (baseline != 0)
    return is_it

print(isclose(0, 0.001, tolerance=0.01))

# consider: a and b
# let's say a is False
# do I care what b is?
