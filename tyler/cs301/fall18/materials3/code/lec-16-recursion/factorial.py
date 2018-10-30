def fact(n):
    if n == 1:
        return 1
    else:
        p = fact(n-1)
        return n * p


f = fact(3)
print('f =', f)
