ship_x = 2
ship_y = 4
x = int(input("enter x: "))
y = int(input("enter y: "))

assert(0 <= x <= width)

hit = ship_x == x and ship_y == y
symbol = str(int(hit))
print("Hit? " + str(hit))

width = 5
height = 5
print(('.' * width + "\n") * y, end="")
print("." * x + symbol + "." * (width - x - 1))
print(('.' * width + "\n") * (height - y - 1))
