guess = -1
answer = 2

if guess == answer:
    print('correct')
else:
    if answer < 0 or answer > 100:
        print('need in 0 to 100 range')
if abs(answer - guess) < 5:
    print('you were close')
