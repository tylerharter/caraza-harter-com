def f():
    yield 1
    yield 2
    yield 3

gen = f()
for x in gen:
    print(x)
