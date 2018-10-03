num = input('Enter a number: ')
num = int(num)

total = 0
count = 0
while num != 999:
    total += num
    count += 1
    num = int(input('Enter a number: '))

average = total / count
print('average =', average)

