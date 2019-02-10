def draw_map(x, y, symbol):
    height = 10
    width = 10
    print(("." * width + "\n") * y, end="")
    print("." * x + symbol + "." * (width - x - 1))
    print(("." * width + "\n") * (height - y - 1))    

def is_hit(x, y):
    ship_x = 5
    ship_y = 3
    hit = x == ship_x and y == ship_y
    return hit
    
def guess():
    x = int(input("x: "))
    y = int(input("y: "))
    hit = is_hit(x, y)
    print("Hit? " + str(hit))
    symbol = str(int(hit))
    draw_map(x, y, symbol)

guess()
