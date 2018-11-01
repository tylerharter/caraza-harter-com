def square(n):
    for x in range(n):
        print('producing square of:', x)
        yield x * x


it = square(3)
for num in it:
    print('printing square:', num)
