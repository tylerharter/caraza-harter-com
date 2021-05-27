# Watch (Part 1)

IFRAME

# Practice

Paste and run the following:

```python
def add(v1, v2):
    return v1 + v2

x = input("Enter x (an int): ")
y = input("Enter y (an int): ")
print("{} + {} is {}".format(x, y, add(x, y)))
```

If you try 3 and 4, you'll get the erroneous message:

```
3 + 4 is 34
```

The problem is that we don't cast the value returned from `input` to
be an int.  But regardless of where the bug is in the code, some
asserts in `add` can help us quickly catch this.

Add `assert type(v1) == int` (and similar for `v2`) to the add
function.  Run again, and take a close look at the runtime exception.

Now, if you like, fix the actual bug by casting `x` and `y` before
passing them as arguments to `add`.

# Questions About the Lecture?

Please ask below.

