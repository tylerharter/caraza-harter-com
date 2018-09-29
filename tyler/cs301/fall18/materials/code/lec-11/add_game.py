import random

def question(x, y):
    answer = input(str(x) + " + " + str(y) + ' = ')
    answer = int(answer)
    if answer == x + y:
        return 1
    else:
        return 0

questions = 20
score = 0
qnum = 1
while qnum <= questions:
    score += question(random.randint(1, 10), random.randint(1, 10))
    qnum += 1

print('Score is ' + str(score))

if score == questions:
    print('Perfect')
elif score >= 0.8 * questions:
    print('Pretty good')
else:
    print('Your addition needs some work')