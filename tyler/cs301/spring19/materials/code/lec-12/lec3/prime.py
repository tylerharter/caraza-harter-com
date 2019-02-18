def is_prime(num):
    i = 2
    while i < num:
        if num % i == 0:
            return False
        i += 1
    return True

start = 1000000
end = 1001000
found_prime = False

i = start
while i <= end:
    if is_prime(i):
        found_prime = True
        break
    i += 1

print("found it?", found_prime)
