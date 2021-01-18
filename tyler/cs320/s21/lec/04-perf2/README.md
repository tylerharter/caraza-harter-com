# Complexity Analysis

## 1. Counting Steps

### Watch: [19-minute video](https://youtu.be/gtUDwbX-7lE)

Which of these three code snippets could qualify as a single step (`words` is a list)?

Snippet 1:
```python
found = "hello" in words
```

Snippet 2:
```python
for word in words:
    print(word)
```

Snippet 3:
```python
for i in range(10):
    print(word[0])
```

<details>
    <summary>ANSWER</summary>
    <p>
    Let's assume N=len(words).  Only snippet 3 qualifies as a single step.  Although it loops 10 times (perhaps slow), that loop doesn't get keep getting slower and slower as N gets larger and larger.  In contrast, looping over every word in the list (as in snippet 2) will get slower as the list gets larger.  Snippet 1 is the same thing: a loop in disguise.
    </p>

</details>

## 2. Big O

### Watch: [18-minute video](https://youtu.be/ZBuLKUQlNWA)

Say we want to show that f(N)=N+5.  We want to show f(N) is in the set
O(g(N)), where g(N)=N.

To show this, we need to pick a multiplier C and a lower bound for N.  Let's
say we pick C=2.  Now, we need to choose a lower bound for N so that the
following is true:

N+5 <= 2*N

What lower bound for N do you choose?

<details>
    <summary>ANSWER</summary>
    <p>
    5 is the smallest N that works (if you plotted N+5 and 2*N on the y-axis, with N on the x-axis, you'll see a crossover point there).
    Any lower bound for N that is greater than 5 also works just fine.
    </p>

</details>

## 3. Prime Example

### Watch: [13-minute video](https://youtu.be/5tDNvh8LO84)

The code we analyzed is a very a tricky case!  Each iteration of loop in
`find_primes` requires more steps than the previous iteration.  So we
get something like `O(1+2+3+...+N)`, or some multiple of that.  This
does NOT reduce to `O(N)`, as might feel intuitive.  Instead, it
reduces to `O(N**2)`.

To see why, look at this figure:

<img src="gauss.png" width=500>

The total number of steps is slightly more than half the area of that
square.

To see the exact formula, paste and compare these two functions for
adding a sequence of consecutive numbers (`high` is inclusive):

```python
def add_v1(low, high):
    nums = range(low, high+1)
    total = 0
    for num in nums:
        total += num
    return total

def add_v2(low, high):
    num_count = high-low+1
    num_avg = (low+high) / 2
    return num_count * num_avg
```

Check that they work the same: run `add_v1(1,10)` and `add_v1(1,10), add_v2(1,10)`.
