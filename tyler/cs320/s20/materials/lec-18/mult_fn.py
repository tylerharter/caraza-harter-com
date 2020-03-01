def mult_fn(num):
    def multiplier(x):
        return x * num
    return multiplier

triple = mult_fn(3)
double = mult_fn(2)

print(triple(10))
print(double(10))
