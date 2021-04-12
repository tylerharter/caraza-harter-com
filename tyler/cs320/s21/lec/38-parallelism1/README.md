# Parallelism 1

## 1. Parallelism Intro

### Watch: [23-minute video](https://youtu.be/aubimxpz5bA)

### Practice: Questions

What is an advantage of GPUs over CPUs?
1. the cores are more flexible
2. the cores are faster
3. there are more cores overall

<details>
    <summary>ANSWER</summary>
    (3) GPUs generally have many more cores, but they are typically slower and less flexible
</details>

In what pattern are there multiple instruction pointers executing different code in the same process?
1. thread parallelism
2. process parallelism
3. GPU parallelism

<details>
    <summary>ANSWER</summary>
    (1) each instruction pointer is associated with a thread, and thread parallelism means there are multiple threads in the same process
</details>


## 2. Pool Map

### Watch: [10-minute video](https://youtu.be/9flI5PSFbAY)

### Practice: String Mult

Consider this code:

```python
nums = [2, 1, 8]
laughs = ["ha"*must for must in nums]
laughs
```

Finish the following to achieve the same result, but with the help of
a pool of 5 processes:

```python
from multiprocessing.pool import Pool

def laugh(mult):
    return ????

with Pool(????) as p:
    laughs = p.map(????, nums)

laughs
```

<details>
    <summary>ANSWER</summary>
    Replace the blanks with <code>"ha"*mult</code>, <code>5</code>, and <code>laugh</code>
</details>


## 3. Parallel Download

### Watch: [6-minute video](https://youtu.be/hbDXqvk9yB0)

### Practice: Pool Size

Try running the following example from lecture with varying pool sizes
(1, 4, 8, etc):

```python
import requests, time
from multiprocessing.pool import Pool

url = "https://tyler.caraza-harter.com/cs320/f20/lectures/lec-17/practice7/{}.html"

def fetch(idx):
    r = requests.get(url.format(idx))
    r.raise_for_status()
    return r.text

fetch(1)

t0 = time.time()
with Pool(????) as p:
    pages = p.map(fetch, range(18))
t1 = time.time()
t1-t0
```

There are 18 requests to be made.  Is the fastest option to have 18
processes in the pool?  Or does the overhead of creating so many
processes out-weight the benefits of increased parallelism?

**Lesson:** If performance of something is important enough (perhaps
because it will be run many times), it might be worthwhile to collect
large samples of request times, with varying pool sizes.  In practice,
it's often good enough to try a few configurations each a few times,
then choose one that seems pretty good.  Getting comfortable running
casual performance experiments like this will make you a better
programmer.

## 4. Debugging

### Watch: [9-minute video](https://youtu.be/A4PUGicNRe4)

### Practice: Process Behavior

Paste and run the following:

```python
from multiprocessing.pool import Pool

msg = "A"

def repeat(n):
    print(msg * n)

# msg = "B"
with Pool(1) as p:
    # msg = "C"
    p.map(repeat, [2,3,5])
```

Remember that a process is pool by initially cloning (copying) the
original process.  This means all variables will start the at the
moment the clone occurs, but may take on different values in the
different processes later.

Question 1: are the processes cloned at the `with Pool(1) as p:` or
the `p.map(repeat, [2,3,5])` line?

Try uncommenting the `msg = ` lines and see if you can infer the
answer.

<details>
    <summary>ANSWER</summary>
    The processes are cloned as soon as the Pool is created.
</details>

When multiple processes are created, will they always run in the same
order?

Try increasing the pool size from 1 to 10, then keep trying to run the
cell a dozen or so times (the `CTRL-ENTER` shortcut makes this easier
than using the `SHIFT-ENTER` shortcut).

<details>
    <summary>ANSWER</summary>
    If you try enough times, you should eventually notice that the order of prints is not always the same.
    The operating system decides the order in which to run the processes, and it may make different
    decisions each time (this decision making is called "scheduling").  Although the order in which
    the processes run may differ, the order of returned values that `p.map` gives back will always
    correspond to the order of inputs.
</details>
