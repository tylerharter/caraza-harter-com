# From Unsolvable to Solvable

## 1. Column Spaces

### Watch: [11-minute video](https://youtu.be/Lf84uF7P4ME)

### Practice: What's in the Space?

Paste this matrix:

```python
X = np.array([
    [5,0,0],
    [0,15,0],
    [0,0,3],
    [-1,-1,-1],
])
X
```

Claim: this column is in the column space of X:

```
array([[15],
       [15],
       [15],
       [-9]])
```

We can prove this by finding a linear combination of the columns of X.
We do so by multiplying the columns of X by the coefficients in the
following vector c.  Try it:

```python
c = np.array([3,1,5]).reshape(-1,1)
X @ c
```

The following is NOT in the column space of X:

```
array([[5],
       [15],
       [3],
       [1]])
```

Can you make an argument why it's not?

<details> <summary>ANSWER</summary> To get a positive (1) in
    that last position, we would need to multiply at least one of the
    columns by a negative.  But any way we might do this would force
    us to have a negative in the 1st, 2nd, or 3rd position, which we
    don't see. </details>

## 2. When `np.linalg.solve` fails

### Watch: [14-minute video](https://youtu.be/uk4m_8PJiU0)

### Practice: Making Bad Matrices

Say a genie appears and gives you a `mystery` function that takes a
row (of size 3) as input and gives back a corresponding output.  The
genie says the function is linear, but does not allow you to see the
code (OK, it's actually below, but play along and don't look at it).

Instead of granting you three wishes, the genie says you can send
three rows as input (`X`) to `mystery` and see the three return values
(`y`).

As a clever numpy user, you run the following to create your own
function, `model`, based on the behavior of `mystery` those three
times.  `model` works just like `mystery`, but you can call it as
often as you like!  (This is the linear algebra equivalent of wishing
for more wishes).

```python
def mystery(row):
    # pretend we can't see this code
    return row[2] - row[0]

X = np.array([
    [1,9,4],
    [1,10,4],
    [1,10,5],
])
y = np.array([[mystery(row)] for row in X])
print("y (outputs):", y)

c = np.linalg.solve(X, y)
print("c coefficients:", c)

def model(row):
    return row @ c

print("model works like mystery!", model(np.array([[1,9,4]])))
print("And we can call it with new values!", model(np.array([[4,5,10]])))
```

This worked out because we tried "good" inputs to `mystery` (which is
not hard, actually -- randomly chosen `X` values will almost
certainly be "good").

Let's try some "bad" inputs and see how `solve` breaks.  "Bad" inputs
are redundant.  Try the following:

1. change the last row from `[1,10,5]` to `[1,10,4]` (so that it's a repeat of the middle row) and run the code.  Take note of the error.
2. now change the last row from `[1,10,5]` to `[2,19,8]`.  This is not obviously redundant, because all the three rows look different, but it will actually break because row three is a sum of the other two (so sending it to `mystery` provides no new information).

## 3. Projection Matrices

### Watch: [18-minute video](https://youtu.be/EuXx49NtC80)

### Practice: Projection

Run the following:

```python
import numpy as np
import pandas as pd
x0 = np.random.normal(20, 5, 30)
x1 = np.random.randint(low=1, high=3, size=30)
noise = np.random.normal(0, 3, 30)
y = x0 * 2 - x1*30 + noise
df = pd.DataFrame({"x0":x0, "x1":x1, "y":y})
df.plot.scatter(x="x0", y="y", c=df["x1"], vmin=0, marker="x")
```

Here, we want to look for the relationship between y (shown on the
y-axis) and x0, x1 (represented as x-axis and color, respectively).

There are two equivalent ways of looking at the problem we face:
1. we're looking for two variables (the coefficients in x by which we multiply x0 and x1), but we have 30 equations (one for each row) that are inconsistent with each other (due to noise)
2. it would not be possible to fit straight lines to the data

Although the `y` column is not a linear combination of the `x0` and
`x1` columns, let's create `p` column that is as close as possible to
`y` while also being a linear combination of the `a` columns.

Complete and run the following (reference the lecture video to get the
formula for the projection matrix):

```python
X = df.values[:, :2]
P = ????
df["p"] = P @ df["y"]

ax=df.plot.scatter(x="x0", y="y", c=df["x1"], vmin=0, marker="x")
df.plot.scatter(x="x0", y="p", c=df["x1"], vmin=0, marker="o", ax=ax)
```

In the scatter plot, note that the circles represent the `p` column we
constructed.  Although we don't solve for the coeficients now, note
that visually this now appears to be a tractable problem.
