counts = {}

def count_me(fn):
    counts[fn.__name__] = 0
    def wrapper():
        counts[fn.__name__] += 1
        fn()
    return wrapper

@count_me
def f():
    print("f")

@count_me
def g():
    print("g")

f()
g()
g()
print(counts)
