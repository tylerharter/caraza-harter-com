# Clutering: K-Means

## 1. K-Means from Scratch

### Watch: [26-minute video](https://youtu.be/Y3xDAR_zGQ8)

### Practice: fit method

Paste the following:

```python
import numpy as np
import pandas as pd
from sklearn import datasets

# x0 => x-axis
# x1 => y-axis
# cluster => marker type
def km_scatter(df, **kwargs):
    ax = kwargs.pop("ax", None)
    if not "label" in df.columns:
        return df.plot.scatter(x="x0", y="x1", marker="$?$", ax=ax, **kwargs)

    for marker in set(df["label"]):
        sub_df = df[df["label"] == marker]
        ax = sub_df.plot.scatter(x="x0", y="x1", marker=marker, ax=ax, **kwargs)
    return ax

class KM:
    def __init__(self, epochs):
        self.epochs = epochs
        
    def fit(self, X):
        self.df = X.copy()

        clusters = np.random.uniform(-5, 5, size=(3,2))
        clusters = pd.DataFrame(clusters, columns=["x0", "x1"])
        clusters["label"] = ["o", "+", "x"]
        self.clusters = clusters
        self.labels = list(self.clusters["label"])

        # TODO: find the centroids!

    def plot(self):
        ax = km_scatter(self.df, s=100, c="0.7")
        km_scatter(self.clusters, s=200, c="red", ax=ax)
        
    # centroids => points (df)
    def assign_points(self):
        for cluster in self.clusters.itertuples():
            x0_diff = df["x0"] - cluster.x0
            x1_diff = df["x1"] - cluster.x1
            dist = (x0_diff**2 + x1_diff**2) ** 0.5
            self.df[cluster.label] = dist
        self.df["label"] = km.df[km.labels].idxmin(axis=1)
        return self
    
    # points => centroids
    def update_centers(self):
        clusters = km.df.groupby("label").mean()
        self.clusters = clusters[["x0", "x1"]].reset_index()
        return self
```

The above code is similar to that in lecture, with a few differences:
1. data is passed to a `fit` method rather than to the `__init__` method
2. `KM` is directly responsible for picking random starting centroids (these aren't passed in anymore)
3. there is an `epochs` parameter passed in

**Step 1**: complete the `fit` method, replacing the `TODO`.  There
should be a loop, and each iteration `assign_points` and
`update_centers` should both be called.  The loop should iterate
`self.epochs` times.  An `epoch` is a fancy word often used in machine
learning to refer to an iteration of a loop in k-means and other
iterative algorithms.

**Step 2**: generate some data

```python
x, y = datasets.make_blobs(n_samples=100, centers=3, cluster_std=1.2)
df = pd.DataFrame(x, columns=["x0", "x1"])
```

**Step 3**: fit the clusters and plot the result (in a new cell)

```python
km = KM(20)
km.fit(df)
km.plot()
```

Experiment with re-running Step 2 a few times to see how k-means
behaves for different data.  Each time you generate new data, re-run
Step 3 several times.

Notice that you sometimes get different results?  This is normal: the
quality of the results often depends on the starting clusters chosen.
In practice, people get around this issue by running k-means many
times (in a loop), only keeping the best results.

## 2. K-Means with sklearn

### Watch: [16-minute video](https://youtu.be/a84UtqVpx08)

### Practice: Cluster Counts

**Step 1**: Generate some clusters:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets

plt.rcParams["font.size"] = 16

coords1, _ = datasets.make_blobs(n_samples=300, centers=1, cluster_std=1)
coords2, _ = datasets.make_blobs(n_samples=300, centers=2, cluster_std=0.8)
coords3, _ = datasets.make_blobs(n_samples=200, centers=3, cluster_std=0.5)
df = pd.DataFrame(np.vstack((coords1, coords2, coords3)), columns=["x0", "x1"])
df.plot.scatter(x="x0", y="x1", c="0.7")
```

**Step 2**: Let's fit a model to those clusters:

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=4)
km.fit(df)
```

**Step 3**: Plot it

```python
ax = df.plot.scatter(x="x0", y="x1", c="0.7")

for i in range(len(km.cluster_centers_)):
    x, y = km.cluster_centers_[i]
    ax.text(x, y, s=i, size=18,
            horizontalalignment="center",
            verticalalignment="center")
```

If it looks like there are too many or too few clusters, go back to
step 2 and tweak `n_clusters`.

Step 4: count points per cluster

Complete the following to produce a bar plot, showing the number of
points per cluster (you can put all of `km`'s predictions in a pandas
Series, making it easy to count the number of occurrences of each
cluster assignment):

```python
counts = pd.Series(????).????
ax = counts.plot.bar(color="0.4")
ax.set_xlabel("Cluster ID")
ax.set_ylabel("Points in Cluster")
```

<details>
    <summary>ANSWER</summary>
    <code>km.predict(df)</code> and <code>value_counts()</code>
</details>

## 3. K-Means for Preprocessing

### Watch: [5-minute video](https://youtu.be/zaAfvHOfxvk)
