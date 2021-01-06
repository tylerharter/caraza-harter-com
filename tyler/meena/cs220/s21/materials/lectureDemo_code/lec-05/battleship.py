width = 10
height = 8

ship_x = 7
ship_y = 3

guess_x = int(input("Enter guess x: "))
guess_y = int(input("Enter guess y: "))

# STEP 1: rows before guess
print(("." * width + "\n") * guess_y, end="")

# STEP 2: guess row
print("." * guess_x, end="")
symbol = int(guess_x == ship_x and guess_y == ship_y)
print(symbol, end="")
print("." * (width - guess_x - 1))

# STEP 3: rows after guess
print(("." * width + "\n") * (height - guess_y - 1))

