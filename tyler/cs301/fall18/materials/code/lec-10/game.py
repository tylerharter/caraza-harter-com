def question(x, y):
    answer = input(str(x) + " + " + str(y) + ' = ')
    answer = int(answer)
    if answer == x + y:
        return 1
    else:
        return 0

score = 0
score += question(10, 20)
score += question(2, 3)
score += question(4, 5)
score += question(10, 20)
print(score)