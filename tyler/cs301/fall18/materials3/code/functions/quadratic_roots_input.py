# Finding the roots of a quadratic equation.
# a * (x ** 2) + b * x + c = 0
# 3 * (x ** 2) + 2 * x - 1 = 0

a = float(input('Enter a: '))
b = float(input('Enter b: '))
c = float(input('Enter c: '))

# Compute the roots of the quadratic equation
x1 = (-b + ((b ** 2) - (4 * a * c)) ** (1/2)) / (2 * a)
x2 = (-b - ((b ** 2) - (4 * a * c)) ** (1/2)) / (2 * a)

print('The roots of the quadratic equation are:')
print(x1)
print(x2)
