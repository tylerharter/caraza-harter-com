# Breadth-First Search

## 1. BFS Backtrace

### Watch: [26-minute video](https://youtu.be/gHQMBJQoY_Q)

## 2. Stacks, Queues, and Priority Queues

### Watch: [24-minute video](https://youtu.be/0Ai6CdtEIEk)

### Practice: heapq and dequeue

First, paste and run the example from lecture:

```python
import time, random
import pandas as pd
import matplotlib.pyplot as plt

iters = 1000

def benchmark_microsec(data, pattern):
    t0 = time.time()
    # measure bad ways to implement the patters (all with a list!)
    for i in range(iters):
        if pattern == "stack":
            data.append(i % 10)
            _ = data.pop(-1)
        elif pattern == "queue":
            data.append(i % 10)
            _ = data.pop(0)
        elif pattern == "prio":
            data.append(i % 10)
            data.sort()
            _ = data.pop(0)
        else:
            raise Exception("pattern not supported")
    t1 = time.time()
    return (t1-t0) / iters * 1e6

df = pd.DataFrame()
for N in [1000,2000,5000,10000]:
    df.loc[N,"stack"] = benchmark_microsec([1]*N, "stack")
    df.loc[N,"queue"] = benchmark_microsec([1]*N, "queue")
    df.loc[N,"prio"] = benchmark_microsec([1]*N, "prio")

plt.rcParams["font.size"] = 16
df.plot.line(ylim=0)
plt.xlabel("N")
plt.ylabel("Microseconds")
```

Now, for "prio", let's use `heapq`.  Make the following changes:

* do `import heapq`
* get rid of the `data.sort()` line
* instead of `data.append(i % 10)`, use `heapq.heappush(data, i % 10)`
* instead of `data.pop(0)`, use `heapq.heappop(data)`

Rerun, and notice how much faster the code is.

Now, for "queue", let's use `dequeue`.  Make the following changes:

* do `from collections import deque`
* instead of `benchmark_microsec([1]*N, "queue")`, use `benchmark_microsec(deque([1]*N), "queue")`
* instead of `data.pop(0)`, use `data.popleft()`

Rerun.  It will be so fast now that you'll probably need to increase
`iters` to a million or so get clean numbers:

<img src="perf.png" width=450>
