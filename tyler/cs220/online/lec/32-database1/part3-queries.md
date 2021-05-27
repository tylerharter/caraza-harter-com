# Watch (Part 3)

IFRAME

# Practice

538 keeps a dataset describing pollsters (who try to predict elections) here: https://github.com/fivethirtyeight/data/tree/master/pollster-ratings

Run this snippet to fetch the dataset into a DataFrame, which is then dumped into a table called `pollsters` in a new database called `pollsters.db`:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("pollsters.db")
df = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/pollster-ratings.csv")
df.loc[:, "Pollster":"Races Called Correctly"].to_sql("pollsters", conn, if_exists="replace")
```

Run this to see some important columns for the first 20 rows (note how columns with spaces in them are surrounded by backticks):

```python
pd.read_sql("""
SELECT Pollster, `Polls Analyzed`, `Races Called Correctly`, `538 Grade` FROM pollsters
LIMIT 20
""", conn)
```

You job is to find the 10 pollsters with the highest percentage of
correctly called races.  Filter to pollsters for which "polls
analyzed" is greater than 15 so that we don't identify new pollsters
who happened to call one race correctly.  Complete the following:

```python
pd.read_sql("""
SELECT *
FROM pollsters
WHERE ????
ORDER BY ????
LIMIT ????
""", conn)

# Questions About the Lecture?

Please ask below.

