import math

def pizza_size(radius):
    return (radius ** 2) * math.pi

def slice_size(radius, slice_count):
    if not radius > 0:
        raise ArithmeticError("negative radius")
    if not slice_count > 0:
        raise ArithmeticError("negative slices")
    total_size = pizza_size(radius)
    return total_size * (1 / slice_count)

def main():
    for i in range(10):
        # grab input
        try:
            args = input("Enter: ")
            argsssss = args.split(',')
            radius = float(args[0].strip()) / 2
            slices = int(args[1].strip())
        except Exception as e:
            print("bad input! err:", str(e))
            print("cause of issue", type(e))
            continue

        # pizza analysis
        try:
            size = slice_size(radius, slices)
            print('PIZZA: radius={}, slices={}, slice square inches={}'
                  .format(radius, slices, size))
        except Exception as e:
            print("analysis err:", str(e))
            print("cause of issue", type(e))
main()








