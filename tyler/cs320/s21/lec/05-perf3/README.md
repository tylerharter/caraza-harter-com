# Sep 16 Lecture

## 1. Upper Bounds

### Watch: [15-minute video](https://youtu.be/Kqygeh-KXDQ)

## 2. List Operation Complexity

### Watch: [23-minute video](https://youtu.be/WKe_oe5fqIU)

### Practice

The performance characteristics of Python sets are different than for
lists.  One different is that `x in DATA` is slow (linear time) if
`DATA` is a list, but fast (constant time) if `DATA` is a set.

Copy+paste tho following code, then add a third measurement where you
see how long it takes to run `-1 in S`.

```python
from pandas import DataFrame
from time import time
import matplotlib
matplotlib.rcParams["font.size"] = 18

# row: different list size
# col: different operation
# cell: how long it took (in microseconds)
df = DataFrame()

S = set()
for i in range(1000):
    S.add(i)
    
    t0 = time()
    x = len(S)
    t1 = time()
    df.loc[len(S), "len"] = (t1-t0) * 1e6
    
    t0 = time()
    x = max(S)
    t1 = time()
    df.loc[len(S), "max"] = (t1-t0) * 1e6

    # TODO: measure how long it takes to run the following, as len(S) increases:
    
ax = df.plot.line()
ax.set_ylim(0, 25)
```

## 3. Sorting and Searching

### Watch: [7-minute video](https://youtu.be/I9T-Fext1j4)
