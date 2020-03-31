import random

with open('short.txt', 'w') as f:
    for i in range(10):
        f.write(str(random.randint(0,100)) + "\n")

with open('nums.txt', 'w') as f:
    # generate 50 million numbers between 0 and 100
    for i in range(50000000):
        f.write(str(random.randint(0,100)) + "\n")