# Watch (Part 2)

IFRAME

# Practice

Create a Series from the distance dictionary to create a plot showing
the distance from Madison, WI to various locations:

```python
import pandas as pd
distance = {
    "Milwaukee": 80,
    "Chicago": 147,
    "Minneapolis": 270,
    "Venus": 24800000,
    "Mars": 33900000,
    "Sun": 94196000,
    "Pluto": 2660000000,
    "Alpha Centauri": 2.5672e+13,
}
ax = pd.Series(????).plot.bar()
ax.set_ylabel("Distance to Madison, WI (miles)")
```

Now pass an argument to `.bar(...)` to use log scale for the y-axis.

# Questions About the Lecture?

Please ask below.

