total = 0
count = 0

while True:
    value = input("enter a score in 0-100 (or q for exit): ")
    if value == 'q':
        break

    # we know that value is not q, let's assume it's a number
    number = int(value)
    if number < 0 or number > 100:
        print('bad input!')
        continue
    total += number
    count += 1
    print(total / count)


print('exiting')