x = ["A", "B", "C"]
y = x

def f(items):
    print(len(items))

f(x)
g = f
g(x)