def is_prime(n):
    i = 2
    while i < n:
        if n % i == 0:
            return False
        i += 1
    return True

start = 1000000
end = 1001000
found_prime = False

i = start
while i <= end:
    if is_prime(i):
        print("debug: found", i)
        found_prime = True
        break
    i += 1
print("did we find one?", found_prime)
