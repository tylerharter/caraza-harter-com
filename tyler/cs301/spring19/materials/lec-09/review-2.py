def h(x=1, y=2):
    print(x, y)  # what is printed?

def g(x, y):
    print(x, y)  # what is printed?
    h(y)

def f(x, y):
    print(x, y)  # what is printed?
    g(x=x, y=y+1)

x = 10
y = 20
f(y, x)
