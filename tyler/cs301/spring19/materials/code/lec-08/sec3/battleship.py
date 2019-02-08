def draw_map(x, y, character):
    width = 10
    height = 10
    print(('.' * width + "\n") * y, end="")
    print("." * x + character + "." * (width - (x + 1)))
    print(('.' * width + "\n") * (height - (y + 1)))

def ship1_hit(x, y):
    ship1_x = 5
    ship1_y = 4
    return (x == ship1_x and y == ship1_y)
    
def ship2_hit(x, y):
    ship2_x = 8
    ship2_y = 8
    return (x == ship2_x and y == ship2_y)
    
def is_hit(x, y):
    return ship1_hit(x, y) or ship2_hit(x, y)

def guess():
    x = int(input("x: "))
    y = int(input("y: "))
    hit = is_hit(x, y)
    print("Hit? " + str(hit))
    symbol = str(int(hit))

    # draw the map
    draw_map(x, y, symbol)

guess()
