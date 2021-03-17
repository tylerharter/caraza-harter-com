# Linear Regression 1

## 1. Machine Learning Intro (Part 1)

### Watch: [22-minute video](https://youtu.be/L62nRsPcRj8)

## 2. Linear Regression (Part 2)

### Watch: [20-minute video](https://youtu.be/86-egKGfoec)

Clearly the population size of a county will be a large factor
determining the number of cases in that county, but how large (one
might speculate that age is also important)?

Let's download a snapshot of the state (this dataset will be simpler
than the one in the demo, as it just shows current totals, not
day-by-day changes).

1. go to https://data.dhsgis.wi.gov/datasets/covid-19-data-by-county
2. click "Download"
3. right-click "Spreadsheet", and click "Copy Link Address..."
4. In SSH, run `wget PASTE_HERE -O wi-snapshot.csv`, replacing `PASTE_HERE` with the URL you copied.

In Jupyter, create a notebook in the same directory, and read in the file:

```python
import pandas as pd
df = pd.read_csv("wi-snapshot.csv").set_index("NAME")
print(df.columns)
df.head()
```

Visualize the relationship between population and cases:

```python
df.plot.scatter(x="POP", y="POSITIVE")
```

Let's measure what portion of variance in POSITIVE cases is explained by POPulation:

```python
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(df[["POP"]], df["POSITIVE"])
lr.score(df[["POP"]], df["POSITIVE"])
```

You should get about 98% -- wow!

What about deaths?  Are those so closely related to population?  You
might expect things like age and quality of hospitals to be a bigger
factor here.  Copy the code from above and modify accordingly.  You
should get about 90%.

## 3. Train/Test Split (Part 3)

### Watch: [5-minute video](https://youtu.be/ldZiGO0C4yg)
