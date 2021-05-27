# Watch (Part 2)

IFRAME

# Practice

Run the following to create a pollsters.db database with a pollsters
table that describes the pollsters tracked by 538:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("pollsters.db")
df = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/pollster-ratings.csv")
df.loc[:, "Pollster":"Races Called Correctly"].to_sql("pollsters", conn, if_exists="replace")
```

538 gives each pollster a letter grade.  How many pollsters are there
with each grade, and what is the average "Races Called Correctly" for
each grade level?

```python
pd.read_sql("""
SELECT ????, COUNT(), AVG(????)
FROM pollsters
GROUP BY ????
""", conn)
```

# Questions About the Lecture?

Please ask below.

