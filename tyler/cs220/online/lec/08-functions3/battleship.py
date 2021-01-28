width = 8
height = 10
ship_x = 3
ship_y = 8

score = 0

def play_round():
    global score
    guess_x = int(input("Enter x: "))
    guess_y = int(input("Enter y: "))
    hit = int(guess_x == ship_x and guess_y == ship_y)
    score = score + hit # 0 or 1

    # step 1: above guess row
    print(("." * width + "\n")*guess_y,
          end="")

    # step 2: guess row
    print("." * guess_x, end="")
    print(str(hit), end="")
    print("." * (width-1-guess_x))

    # step 3: after guess row
    print(("." * width + "\n")*(height-1-guess_y),
          end="")

play_round()
play_round()
play_round()
print("FINAL SCORE:", score)
