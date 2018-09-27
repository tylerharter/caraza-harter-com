last_num = input('Enter a number: ')
last_num = int(last_num)

total = 0
num = 1

while num <= last_num:
    total += num
    num += 1

print('sum up to', last_num, '=', total)