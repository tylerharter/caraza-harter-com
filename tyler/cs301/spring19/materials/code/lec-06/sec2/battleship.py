ship_x = 5
ship_y = 3
x = int(input("x: "))
y = int(input("y: "))
hit = x == ship_x and y == ship_y
print("Hit? " + str(hit))
symbol = str(int(hit))

height = 10
width = 10
print(("." * width + "\n") * y, end="")
print("." * x + symbol + "." * (width - x - 1))
print(("." * width + "\n") * (height - y - 1))
