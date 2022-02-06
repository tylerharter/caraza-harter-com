def f():
    print("A")
    yield 1
    print("B")
    yield 2
    print("C")
    yield 3

for x in f():
    print(x)