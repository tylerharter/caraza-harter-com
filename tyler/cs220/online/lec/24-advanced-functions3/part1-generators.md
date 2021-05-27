# Watch (Part 1)

IFRAME

# Practice

Paste and run the following:

```python
def get_user_nums():
    nums = []
    for i in range(5):
        num = input("Enter an int (or 'q' to exit): ")
        if num == "q":
            break
        nums.append(int(num))
    return nums

total = 0
for num in get_user_nums():
    total += num
    print("Total:", total)
```

Let's turn `get_user_nums` into a generator function so that (a) we
can get a running total as we go, and (b) there is no limit on how
many number can be entered.

1. instead of appending `int(num)` to a list, `yield` it.
2. delete the `nums = []` and `return nums` lines
3. replace `for i in range(5):` with `while True:`

Try it out!

# Questions About the Lecture?

Please ask below.
