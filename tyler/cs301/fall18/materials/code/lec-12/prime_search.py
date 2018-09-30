from prime import *

print('\nthis program tells you whether ' +
      'a range of integers contains a ' +
      'prime number\n')

start = int(input('range start: '))
end = int(input('range end: '))

found_prime = False
i = start
while i <= end:
    print('check ' + str(i))
    if is_prime(i):
        print('it is prime!')
        found_prime = True
    i += 1

if found_prime:
    print('YES')
else:
    print('NO')