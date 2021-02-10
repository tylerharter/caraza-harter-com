def divide(top, bottom):
    return top/bottom

def flip_div(top=1, bottom=2, flip=False):
    if flip:
        return divide(top=bottom, bottom=top)
    else:
        return divide(top=top, bottom=bottom)

x = 2
y = 3
print(flip_div(x, y, True))
