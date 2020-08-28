width = 10
height = 8

ship_x = 3
ship_y = 5

guess_x = int(input("enter x:"))
guess_y = int(input("enter y:"))

# rows above guess
print(("." * width + "\n") * (guess_y), end="")

# partial row before guess
symbol = str(int(ship_x == guess_x and ship_y == guess_y))
print("." * guess_x + symbol + "." * (width-guess_x-1))

# rows below guess
print(("." * width + "\n") * (height - guess_y - 1))

print("Hit?")
print(ship_x == guess_x and ship_y == guess_y)
