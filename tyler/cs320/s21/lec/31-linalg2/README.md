# Linear Algebra 2

## 1. Predicting with Dot Product

### Watch: [15-minute video](https://youtu.be/mcoBwT5U-Wk)

### Practice: Matrix dot Vector

Run and practice the following until you can get three in a row.

So this doesn't get tedious, we only make you find one number in the
resulting vector, though you should be able to compute the whole
vector if asked.

To compute a single 'x' value, you'll need to look at all the values
in the vector `b`, but you'll only need to look at a single row of `A`
(you can ignore the other rows).  So your first step should be to
identify that row, based on what row 'x' is in.

```python
def practice(cols):
    rows = np.random.randint(3, 7)
    X = np.random.randint(-3,4,(rows, cols))
    c = np.random.randint(-3,4,cols).reshape(-1,1)
    print("X = ")
    print(X)
    print()
    print("c = ")
    print(c)
    print()
    M = (X @ c).astype(object)
    pos = np.random.randint(0,rows)
    expected, M[pos,0] = M[pos,0], "?"
    print("X @ c = ")
    print(M)    
    print()
    answer = int(input("What is '?'?  "))
    print()
    if answer == expected:
        print("Good job!")
        return True
    else:
        print("\nActually, it is ", expected)
        print("Calculation:", " + ".join(f"({x}*{y})" for x,y in zip(X[pos].reshape(-1), c.reshape(-1))))
        time.sleep(2)
        return False

goal = 3
correct = 0
while correct < goal:
    print("="*40)
    print(f"Get {goal-correct} in a row correct to finish!")
    print("="*40)
    print()
    if practice(correct+2):
        correct += 1
    else:
        correct = 0
    print()
        
print(f"Nice, you got {goal} in a row correct!")
```

## 2. Solving Equations

### Watch: [13-minute video](https://youtu.be/3z3ZzCY2RpA)

### Practice: Pricing Fruits

Say you're running an auction selling fruit baskets.  The baskets
contain apples and bananas.

The baskets are pretty cool, so people would pay something even for an
empty basket (even though they are never for sale individually).

You want to put a dollar value on apples, bananas, and baskets.

Let's say you've sold three baskets:

* 10 apples and 0 bananas sold for $7
* 2 apples and 8 bananas sold for $5
* 4 apples and 4 bananas sold for $5

This data gives us three variables and three equations:

* `10*apple + basket == 7`
* `2*apple + 8*banana + basket == 5`
* `4*apple + 4*banana + basket == 5`

Complete the following to find the individual value of each item:

```python
import numpy as np

X = np.array([
    [10,0,1],
    [???,8,1],
    [4,4,???],
])
y = np.array([7,5,???]).reshape(-1,1)

c = np.linalg.solve(X, y)
apple_val, banana_val, basket_val = c.reshape(-1)

print("Apple Value:", apple_val)
print("Banana Value:", banana_val)
print("Basket Value:", basket_val)
```

<details>
    <summary>ANSWER</summary>
    Apples are worth $0.50; bananas, $0.25; baskets, $2
</details>

## 3. Column Perspective of Dot Product

### Watch: [17-minute video](https://youtu.be/YsAxY90Jd3c)

### Practice: Column Subtraction

Paste the following:

```python
import numpy as np

X = np.array([
    [100,10,3],
    [200,10,2],
    [300,10,1]
])

def col_dot(M, v):
    col_sum = np.zeros((len(M), 1))
    for col_idx in range(M.shape[1]):
        col = M[:, col_idx:col_idx+1] * v[col_idx,0]
        #print(col, "\n")
        col_sum += col
    return col_sum

c = np.array([???,???,???]).reshape(-1,1) # TODO
col_dot(X, c)
```

Let's say we want to subtract the third column from the first column
(this is a linear combination!) to get values 97, 198, and 299.

Replace the `???` parts with numbers to achieve this subtraction.

<details>
    <summary>ANSWER</summary>
    <code>c = np.array([1,0,-1]).reshape(-1,1)</code>
</details>
