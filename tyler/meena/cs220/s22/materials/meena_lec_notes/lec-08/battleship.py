width = 10
height = 8

ship_x = 7
ship_y = 3

total_score = 0

def play_battleship():
    global total_score
    
    guess_x = int(input("Enter guess x: "))
    guess_y = int(input("Enter guess y: "))

    # STEP 1: rows before guess
    print(("." * width + "\n") * guess_y, end="")

    # STEP 2: guess row
    print("." * guess_x, end="")
    symbol = int(guess_x == ship_x and guess_y == ship_y)
    print(symbol, end="")
    print("." * (width - guess_x - 1))

    # this computation will not work without global declaration
    # why? 
    # recall that total_score += symbol is short form for total_score = total_score + symbol
    # on the left hand side of the above expression you are assigning new value to the variable
    # total_score, which is not possible without first initializing a value (to local variable)
    total_score += symbol 

    # STEP 3: rows after guess
    print(("." * width + "\n") * (height - guess_y - 1))

play_battleship()
play_battleship()
play_battleship()
print("Total score is:", total_score)
