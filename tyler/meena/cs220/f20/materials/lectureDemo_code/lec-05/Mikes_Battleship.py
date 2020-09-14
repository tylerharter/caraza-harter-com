width = 8
height = 10

ship_x = 4
ship_y = 4

guess_x = input("Enter your x-guess: ")
guess_y = input("Enter your y-guess: ")
guess_x=int(guess_x)
guess_y=int(guess_y)

hit = guess_x==ship_x and guess_y==ship_y
hit =int(hit)
symbol = "*"*hit + "O"*((hit+1)%2)

# step 1 rows before the guess
print(("."*width +"\n") * guess_y, end="")

# step 2 guess row
print("."*guess_x, end="")
print(symbol, end="")
print("."*(width-guess_x-1))

# step 3 rows after the guess
print(("."*width +"\n") * (height-guess_y-1))




