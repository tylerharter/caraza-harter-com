# Watch (Part 2)

IFRAME

Below is a dictionary of the years in which recent named hurricanes
hit Florida (pulled from Wikipedia).  Convert the dictionary to a
pandas Series, then use boolean indexing to quickly identify the names
of all the hurricanes that occured after 2015.

```python
import pandas as pd

hurricanes = {
    "Charley": 2004,
    "Frances": 2004,
    "Ivan": 2004,
    "Jeanne": 2004,
    "Dennis": 2005,
    "Katrina": 2005,
    "Rita": 2005,
    "Wilma": 2005,
    "Hermine": 2016,
    "Matthew": 2016,
    "Irma": 2017,
    "Michael": 2018,
    "Sally": 2020,
}

hurricanes = pd.????(hurricanes)
hurricanes[????]
```

For a challenge, now use the `&` operator to identify all the
hurricanes that occured between 2015 and 2018 (inclusive).

# Questions About the Lecture?

Please ask below.

