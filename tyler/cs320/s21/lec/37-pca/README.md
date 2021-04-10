# Principal Component Analysis

PCA is an unsupervised learning technique for discovering underlying
patterns in the variation across cells in a matrix.  Not only can this
help us understand the data, it can also help us compress our datasets
to save storage space.

## 1. Singular Value Decomposition

### Watch: [12-minute video](https://youtu.be/nva46bNSADs)

### Practice: Matrix Factors

Imagine a matrix X had been factored into parts with this:

```python
u,s,vh = np.linalg.svd(X, full_matrices=False)
```

Then, somebody gave you the three parts, but not the original matrix X
-- paste+run the following:

```python
import numpy as np

u = np.array([[-0.21483724,  0.88723069,  0.40824829],
              [-0.52058739,  0.24964395, -0.81649658],
              [-0.82633754, -0.38794278,  0.40824829]])
s = np.array([16.84810335261421, 1.06836951455471, 0])
vh = np.array([[-0.47967118, -0.57236779, -0.66506441],
               [-0.77669099, -0.07568647,  0.62531805],
               [-0.40824829,  0.81649658, -0.40824829]])
```

Do the multiplications (replacing `????`) necessary to reconstruct the
original matrix, then display it, rounded to 2 decimal places:

```python
X = ????
np.round(X, 2)
```

<details>
    <summary>ANSWER</summary>
    <code>
X = (u*s)@vh
    </code>
</details>

## 2. Compression with SVD

### Watch: [19-minute video](https://youtu.be/HkI1Rml2dWs)

## 3. PCA with sklearn

### Watch: [17-minute video](https://youtu.be/cbslrjMXBVg)

### Practice: Scatter Plot

Sometimes, it is useful to identify the single most important
principal component.  Reducing many columns down to one will allow us
to produce a scatter plot and perhaps perform a regression that is
easy to visualize.

Generate some data:

```python
import numpy as np
import pandas as pd

x = np.random.uniform(0,100,size=50) # hidden
y = 20 - x # want to predict this
x1 = 2*x
x2 = 10-3*x
x3 = 20+x
df = pd.DataFrame({"x1":x1, "x2":x2, "x3":x3, "y":y})
noise = np.random.normal(scale=10, size=df.shape)
df += noise
df.head()
```

Note that we don't have an `x` column in our DataFrame.  We do have
`x1` through `x3` columns that all vary together, and a related `y`
variable.

Can we reduce the 3 x variables back to single variable, a pc1 column
(Principal Component 1)?

Try it:

```python
from sklearn.decomposition import PCA
pca = PCA(????)
df["pc1"] = pca.fit_transform(df[[????]])
df.head()
```

<details>
    <summary>ANSWER</summary>
Pass in <code>1</code> for the first <code>????</code> and pass in <code>"x1", "x2", "x3"</code> for the second <code>????</code>
</details>

Now you have one variable to plot y against:

```python
df.plot.scatter(x="pc1", y="y", color="red")
```

Was that a good idea, or are we missing patterns by collapsing three
variables to one?  Let's check:

```python
pca.explained_variance_ratio_
```

A number close to 1 means that we're capturing most of the
co-variance.  Looks like we're good!
