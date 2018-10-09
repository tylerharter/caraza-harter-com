def add_elements(l):
    total = 0
    for elem in l:
        total += elem
    return total


nums = [1, 2, 7, 10]
total = add_elements(nums)
print('total =', total)


