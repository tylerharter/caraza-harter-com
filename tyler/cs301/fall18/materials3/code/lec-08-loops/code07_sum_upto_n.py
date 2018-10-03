num = input('Enter a number: ')
num = int(num)

total = 0
count = num

while num > 0:
    total += num
    num -= 1

print('sum up to', count, '=', total)

average = total / count

print('average up to', count, '=', average)