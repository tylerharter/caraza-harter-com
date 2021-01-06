def f():
    yield 1
    yield 2
    yield 3

for x in f():
    for y in f():
        print(x, y)