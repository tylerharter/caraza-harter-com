total = 0
count = 0

while True:
    num = int(input('Enter a number: '))
    if num == 999:
        break
    total += num
    count += 1

average = total / count
print('average =', average)

