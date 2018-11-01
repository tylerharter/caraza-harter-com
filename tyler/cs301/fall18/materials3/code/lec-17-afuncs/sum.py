path = "nums.txt"
f = open(path)

numbers = list(f)
total = 0
for num in numbers:
    total += int(num)

print('total =', total)

