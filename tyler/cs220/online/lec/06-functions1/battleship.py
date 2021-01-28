width = 8
height = 10

guess_x = 7
guess_y = 9

# step 1: above guess row
print(("." * width + "\n")*guess_y,
      end="")

# step 2: guess row
print("." * guess_x, end="")
print("X", end="") # TODO: choose symbol for hit/miss
print("." * (width-1-guess_x))

# step 3: after guess row
print(("." * width + "\n")*(height-1-guess_y),
      end="")
