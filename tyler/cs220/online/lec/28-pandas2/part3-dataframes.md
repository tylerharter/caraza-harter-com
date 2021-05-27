# Watch (Part 3)

IFRAME

# Practice

538 has datasets about college major and jobs here: https://github.com/fivethirtyeight/data/tree/master/college-majors.  Fetch the data into a DataFrame:

```python
import pandas as pd
df = pd.read_csv("https://github.com/fivethirtyeight/data/raw/master/college-majors/recent-grads.csv")
df.head()
```

Now, use boolean indexing to find the four majors in the education
category that have an unemployment rate below 4%.

```python
df[(????) & (????)]
```

# Questions About the Lecture?

Please ask below.
