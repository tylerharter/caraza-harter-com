import random

# returns 1 point (for correct)
# returns 0 points (for incorrect)
# returns None (for quit)
def question(x, y):
    answer = input(str(x) + " + " + str(y) + ' = ')
    if answer == 'q':
        return None
    answer = int(answer)
    if answer == x + y:
        return 1
    else:
        return 0

score = 0
questions = 0

result = question(random.randint(1, 10), random.randint(1, 10))

while result != None:
    score += result
    questions += 1
    result = question(random.randint(1, 10), random.randint(1, 10))


print('Score is ' + str(score) + ' of ' + str(questions))

if score == questions:
    print('Perfect')
elif score >= 0.8 * questions:
    print('Pretty good')
else:
    print('Your addition needs some work')