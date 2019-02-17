def is_ship1(x, y):
    ship_x1 = 1
    ship_y1 = 2
    ship_x2 = 5
    ship_y2 = 2
    if ship_x1 <= x <= ship_x2:
        if ship_y1 <= y <= ship_y2:
            return True
    return False

def is_ship2(x, y):
    ship_x1 = 10
    ship_y1 = 5
    ship_x2 = 10
    ship_y2 = 7
    if ship_x1 <= x <= ship_x2:
        if ship_y1 <= y <= ship_y2:
            return True
    return False

# return True if location overlaps with
# any of the ships
def is_ship(x, y):
    return is_ship1(x, y) or is_ship2(x, y)

def draw_map(guess_x, guess_y):   
    height = 8
    width = 12

    hit = is_ship(guess_x, guess_y)

    row = 0
    while row < height:
        col = 0
        while col < width:
            symbol = "."
            if row==guess_y and col==guess_x:
                if hit:
                    symbol = "+"
                else:
                    symbol = "-"
            elif is_ship(col, row):
                symbol = "*"
            print(symbol, end="")
            col += 1
        # END: while
        print()
        row += 1
    # END: while

def main():
    # get input from user
    guess_x = int(input("x: "))
    guess_y = int(input("y: "))
    draw_map(guess_x=guess_x,
             guess_y=guess_y)

main()
