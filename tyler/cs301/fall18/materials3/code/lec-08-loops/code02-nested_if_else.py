num = input('Enter a number: ')
num = int(num)

if num % 2 == 0:
    print(num, 'is divisible be 2')
    if num % 3 == 0:
        print(num, 'is divisible by 3')
        print(num, 'is divisible by 6')
    else:
        print(num, 'is NOT divisible by 3')
        print(num, 'is NOT divisible by 6')
else:
    print(num, 'is NOT divisible be 2')
    print(num, 'is NOT divisible be 6')