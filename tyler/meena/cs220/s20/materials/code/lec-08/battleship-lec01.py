width = 10
height = 8
ship_x = 3
ship_y = 5
score = 0

def is_hit(guess_x, guess_y):
    return ship_x == guess_x and ship_y == guess_y

def play_round():
    global score
    guess_x = int(input("enter x:"))
    guess_y = int(input("enter y:"))
    hit = is_hit(guess_x, guess_y)
    score = score + int(hit)
    
    print(("." * width + "\n") * (guess_y), end="") # rows above guess
    symbol = str(int(hit))
    print("." * guess_x + symbol + "." * (width-guess_x-1)) # guess row
    print(("." * width + "\n") * (height - guess_y - 1)) # rows below guess

play_round()
play_round()
play_round()
print("Final Score:", score)
