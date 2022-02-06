last_b = None

def divide(t, b=None):
    global last_b
    if b == None:
        b = last_b
    last_b = b
    return t / b

print(divide(1, 4))
print(divide(2))
