# Inheritance

## 1. Review Methods

### Watch: [14-minute video](https://youtu.be/A5bbhTWzUoo)

## 2. Context Managers

### Watch: [13-minute video](https://youtu.be/2sup54JwyFQ)

### Practice:

Complete the following code.  The goal is that if code runs inside a
`with` statement using a `TimeIt` context manager, then the time it
took to run will be printed afterwards.

```python
import time

class TimeIt:
    def ????(self):
        self.t0 = time.time()
    
    def __exit__(self, exc_type, exc_value, traceback):
        ????
        print(f"that took {(self.t1-self.t0)*1000} milliseconds")

with TimeIt():
    # add one million numbers
    total = 0
    for i in range(1000000):
        total += i
```

## 3. Inheritance

### Watch: [22-minute video](https://youtu.be/qxqTwFmq8FE)

### Practice:

Create a new string type (`SmartStr`) that inherits most features from
the regular string type, but overrides equality checks so that `x ==
y` will be True if the strings are equal, ignoring case.

```python
class SmartStr(????):
    def __eq__(self, other):
        return ????

x = SmartStr("hello")
y = SmartStr("HELLO")
print(x, y)
x == y # should be True
```

<details>
    <summary>ANSWER</summary>
    <p>
    <b>str</b> and <b>self.lower() == other.lower()</b>
    </p>
</details>
