import math

def pizza_size(radius):
    return (radius ** 2) * math.pi

def slice_size(radius, slice_count):
    assert radius > 0
    assert slice_count > 0
    total_size = pizza_size(radius)
    return total_size * (1 / slice_count)

def main():
    for i in range(10):
        # grab input
        try:
            args = input("Enter pizza diameter(inches), slice count): ")
            args = args.split(',')
            radius = float(args[0].strip()) / 2
            slices = int(args[1].strip())
        except (IndexError, ValueError) as e:
            print("bad input!", type(e))
            continue

        # pizza analysis
        try:
            size = slice_size(radius, slices)
            print('PIZZA: radius={}, slices={}, slice square inches={}'
                  .format(radius, slices, size))
        except Exception as e:
            print("bad math", str(e))

main()
