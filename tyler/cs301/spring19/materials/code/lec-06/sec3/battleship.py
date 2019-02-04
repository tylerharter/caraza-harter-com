

# get location and determine if a hit
ship_x = 5
ship_y = 4
x = int(input("x: "))
y = int(input("y: "))
hit = (x == ship_x and y == ship_y)
print("Hit? " + str(hit))
symbol = str(int(hit))

# draw the map
width = 10
height = 10
print(('.' * width + "\n") * y, end="")
print("." * x + symbol + "." * (width - (x + 1)))
print(('.' * width + "\n") * (height - (y + 1)))
