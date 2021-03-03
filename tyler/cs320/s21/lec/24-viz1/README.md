# Visualization 1

## 1. Matplotlib Coordinate Systems (Part 1)

### Watch: [22-minute video](https://youtu.be/MT0NhmKhLGs)

### Practice: scatter, from scratch

Paste+run the following:

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame([
    {"x":0.1, "y":0.4},
    {"x":0.2, "y":0.2},
    {"x":0.3, "y":0.1},
    {"x":0.4, "y":0.3}
])
df
```

Now paste+run this:

```python
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(7, 4))
ax2.set_xlim(0.1, 0.6)

points1 = ax1.transData.transform(df[["x", "y"]].values) / fig.dpi
print(points1)

def scatter(ax, points):
    for x, y in points:
        p = plt.Circle((x, y), 0.1, facecolor="blue",
                       transform=fig.dpi_scale_trans)
        ax.add_artist(p)

scatter(ax1, points1)
```

`AxesSubplot.transData.transform` can convert an array of points from
the coordinate system of the AxesSupblot to absolute coordinates, in
DPI.  Dividing by `fig.dpi` then gives us inches, which are used by
the above `scatter` method.

Can you modify the above code so it draws the same scatter points as
black dots on the right?  It ought to look like this:

<img src="scatter.png" width=500>

You'll need to (1) make another `.transform` call based on the `ax2`
coordinate system, (2) make an additional call to `scatter`, and (3)
add a parameter to `scatter` to control the `facecolor`.

Remember to also prevent matplotlib from cropping the figure after the coordinates are determined:

```python
%config InlineBackend.print_figure_kwargs={"bbox_inches": None}
```

## 2. Plot Annotations (Part 2)

### Watch: [26-minute video](https://youtu.be/p8rOp-UgxWY)

### Practice: labeled-lines plotter

The example I give in lecture wasn't very general (it wouldn't work if
I had additional columns plotted as lines, for example).  In this
practice, you'll complete a function that makes lines with labels for
any DataFrame, with any numbers of columns.

First, paste the following for some generic setup and to generate a
3-column DataFrame:

```python
from numpy.random import normal
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

matplotlib.rcParams["font.size"] = 16

df = pd.DataFrame({
    "X": normal(10, 20, 100),
    "Y": normal(15, 20, 100),
    "Z": normal(5, 5, 100),
}, index=range(0,100)).cumsum()

df
```

Second, paste+complete the following:

```python
def labeled_lines(df, xlabel="label me", ylabel="label me"):
    ax = df.plot.line(legend=????)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    
    last_x = df.index[-1]
    for i in range(len(df.columns)):
        last_y = df.iloc[-1, ????]
        line_name = df.columns[????]
        ax.text(last_x, last_y, line_name, va="center", ha="left")
    return ax

labeled_lines(df)
```
