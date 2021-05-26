# Watch (Part 2)

IFRAME

# Practice

Copy/paste the factorial example from lecture:

```python
def fact(n):
    if n == 1:
        return 1
    p = fact(n-1)
    return n * p
```

Try calling it with -1 and make a note of the error (so that you'll
quickly recognize infinite recursion errors in the future).

Factorials are often useful for counting different possible orderings.
For example, there are 5*4*3*2*1 possible orders in which 5 people
could stand in line.

Sometimes it's useful to multiply a similar sequence of numbers,
without going all the way to 1.  For example: 5*4*3.  We can adapt our
`fact` function to support this, but now the base case won't always be
`n=1`.

Modify the function so that it starts like this:

```python
def fact(n, stop):
```

Make other changes as necessary.  A call to `fact(5, 3)` should return
60 (5*4*3).

The first two lines will need to use the new `stop` parameter.  When
`fact` calls itself, it will need to pass `stop` to itself.

After the improved function is working, consider giving `stop` a
default argument (`stop=1` in the definition line) so that the
programmers who just want the regular use case (`N*...*1`) don't need
to worry about `step` while allowing other programmers specify the
`stop` as needed for their use case.

# Questions About the Lecture?

Please ask below.

