# Watch (Part 2)

IFRAME

# Practice

Create a program named `adder.py` that we can run like this:

`python3 adder.py 1 2 3`

And it will print 6.  It should similarly work with any number of inputs.

Complete the following in a file named `adder.py`:

```python
import sys
print(sys.argv)

nums = []
for arg in sys.argv[????]:
    nums.append(????)

print(sum(nums))
```

Hints:
* `sys.argv` is a list, and the first entry (`sys.argv[0]`) will be the program name, "adder.py".  Use a slice to get the values in `sys.argv` from position 1 onwards.
* everything in `sys.argv` is a string, so the `arg` variable will contain a string at all times.  We want to add ints to nums, not strings, so use `int(????)` to convert the type.

# Questions About the Lecture?

Please ask below.

