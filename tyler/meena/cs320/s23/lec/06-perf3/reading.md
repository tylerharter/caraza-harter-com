# Iterators and Generators

In the following, pay close attention to how these four definitions,
which often get confused
1. iterator
2. iterable
3. generator function
4. generator object

For these examples, first create a file with numbers 100 to 1:

```python
with open("nums.txt", "w") as f:
    for i in range(100, 0, -1):
        f.write(str(i) + "\n")
```

## Iterators and Iterables

When you call `open(...)` to read a file, you get back a file object.
File objects are *iterators*, meaning you can call `next` on them:

```python
with open("nums.txt") as f:
    print(next(f))
    print(next(f))
    print(next(f))
```

A `list` object IS NOT an iterator, as Python will quickly complain
if you try running the following (`TypeError: 'list' object is not an
iterator`):

```python
nums = [100, 99, 98, 97]
print(next(nums))
print(next(nums))
print(next(nums))
```

However, a `list` object IS an *iterable*, meaning we can call `iter`
to get a different object that is an iterator.

```python
nums = [100, 99, 98, 97]
it = iter(nums)
print(next(it))
print(next(it))
print(next(it))
```

When we see a `for` loop `for x in SOME_OBJECT:`, it does two things automatically:
1. call `iter(SOME_OBJECT)` to get an iterator object from `SOME_OBJECT` (this implies `SOME_OBJECT` must be an iterable)
2. repeatedly call `next` on the iterator object, placing each value in `x`, until there are no more values

## Generator Functions and Generator Objects

You'll sometimes read about "generators" -- we avoid that simple
phrasing in this course because it is often used ambiguously to refer
to either generator functions or generator objects.

You've probably written functions like this many times (replacing `XXXX`, `YYYY`, and `ZZZZ` with something else):

```python
def f():
    some_list = []
    for XXXX in YYYY:
        ...
        some_list.append(ZZZZ)
    return some_list
```

You might elsewhere call such a function to get values over which to
loop (`for x in f():`).

Generator functions are a useful alternative in such use cases; `g` is
very similar to `f` above:

```python
def g():
    for XXXX in YYYY:
        ...
        yield ZZZZ
```

`g` is a *generator function* because it has a yield statement
(instead of the append we saw earlier).  Even though there is no
`return` statement anymore, `g` will return a *generator object* when
called, which is a good alternative to a list in some scenarios:

* `for x in g():` **still works** because generator objects are both iterators and iterables
* `g()[3]` **won't work** anymore because you can't index into generator objects

As long as we don't need indexing, generators have several advantages:

* the code is often a little shorter (and maybe more intuitive, once you get used to the idea)
* if `some_list` in `f` is too big to fit in memory (RAM!), the generator alternative will save us because that approach never has all the `ZZZZ` values in memory at once
* even more extreme, if you want to produce an infinite number of results, generators will still work

The cool thing about the following generator function is that it will
work even the entire `nums.txt` (which is in **storage**) is too big
to fit in **memory** all at once.  It's not unusual for storage space
to be hundreds of times bigger than memory space, so this is an
important technique when working with big datasets.

```python
def rolling_sum():
    total = 0
    with open("nums.txt") as f:
        for line in f:
            total += int(line)
            yield total

for x in rolling_sum():
    print(x)
```

Here's an example of a generator that produces an infinite number of
results.  If you run this one, you'll need to click "Interrupt" under
the "Kernel" menu in Jupyter if you don't want it to run forever.

```python
def even_nums():
    x = 0
    while True:
        yield x
        x += 2

for x in even_nums():
    print(x)
```
