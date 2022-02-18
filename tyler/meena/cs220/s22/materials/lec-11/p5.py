num = 3
while num <= 5:
    is_prime = True
    potential_factor = 2
    while potential_factor < num:
        if num % potential_factor == 0:
            is_prime = False
            break
        potential_factor += 1
    if is_prime:
        print(str(num) + ' is prime')
    else:
        print(str(num) + ' is not')
    num += 1
