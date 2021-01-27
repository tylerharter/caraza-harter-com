width = 8
height = 10
ship1_x = 3
ship1_y = 8
ship2_x = 7
ship2_y = 4

score = 0

def is_hit(guess_x, guess_y):
    if guess_x == ship1_x and guess_y == ship1_y:
        return True
    elif guess_x == ship2_x and guess_y == ship2_y:
        return True
    # else:
    return False

def play_round():
    global score
    guess_x = int(input("Enter x: "))
    guess_y = int(input("Enter y: "))
    if not (0 <= guess_x < width and 0 <= guess_y < height):
        print("Guess within the bounds!")
        return # bad input
    
    if is_hit(guess_x, guess_y):
        score += 1
        symbol = "H"
        print("Nice job, Hit!")
    else:
        symbol = "M"
        print("Sorry, that was a Miss!")

    # step 1: above guess row
    print(("." * width + "\n")*guess_y,
          end="")

    # step 2: guess row
    print("." * guess_x, end="")
    print(symbol, end="")
    print("." * (width-1-guess_x))

    # step 3: after guess row
    print(("." * width + "\n")*(height-1-guess_y),
          end="")

play_round()
play_round()
play_round()
print("FINAL SCORE:", score)
