import math

def pizza_size(radius):
    return (radius ** 2) * math.pi

def slice_size(radius, slice_count):
    if not radius > 0:
        raise ArithmeticError("yikes, negative radius!")
    if not slice_count >= 1:
        raise ArithmeticError("bad slice count!")
    total_size = pizza_size(radius)
    return total_size * (1 / slice_count)

def main():
    for _ in range(10):
        
        # grab input
        try:
            args = input("Enter: ")
            args = args.split(',')
            radius = float(args[0].strip()) / 2
            slices = int(args[1].strip())
        except (IndexError, ValueError) as e:
            print("bad input!", str(e), type(e))
            continue

        # pizza analysis
        try:
            size = slice_size(radius, slices)
            print('PIZZA: radius={}, slices={}, slice square inches={}'
                  .format(radius, slices, size))
        except Exception as e:
            print("math error!", str(e), type(e))
            

main()
