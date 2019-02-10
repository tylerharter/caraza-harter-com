def f():
    x = 1
    y = 2
    z = 3
    if z > x:
        print("A")
        if z == x + y:
            print("B")
            print("C")
        print("D")
        if x == y:
            print("E")
            print("F")
        else:
            print("G")
    elif z == x:
        if x == 1:
            if y == 2:
                if z == 3:
                    print("H")


def g():
    print("I")
    print("J")

f()
g()