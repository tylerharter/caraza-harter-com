# Watch (Part 3)

IFRAME

# Practice

In most board games (like Monopoly) that involve rolling two dice, you
sum the two numbers (and then perhaps move than many spaces); many
know that the average roll in such games will be 7.

What if you're playing a game where you need to **multiply** the
numbers on the two dice to get a total (instead of adding)?  What will
the average be?

First, complete a function that randomly rolls two dice, then returns
the multiplication of the two values.  Test it a few times.

```python
import random

def roll():
    roll1 = random.randint(1, 6)
    roll2 = ????
    return ????

roll()
```

Now, complete a `for` loop that uses your function to estimate the average:

```python
how_many = 1000000
total = 0
for ????:
    total += roll()

avg = total / how_many
print(avg)
```

# Questions About the Lecture?

Please ask below.

