# Watch (Part 1)

IFRAME

# Practice

The USGS publishes earth data in JSON format on their website.  For
example, by carefully constructing the URL, you can request the
earthquakes on a specific day.  Try visiting this:

https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2021-01-01&endtime=2021-01-02

This will list earthquakes that occured on Jan 1, 20201 (the start
date is inclusive, the end date is exclusive).

Complete the following to request content for the above URL and to
check that no error status is returned.

```python
import requests
r = requests.get(????)
r.raise_for_????()
```

Parse the JSON data to a Python dictionary:

```python
earthquakes = r.????()
```

Each earthquake is described by a dictionary in a list.  The following
loops over each earthquake dict, printing the available keys.

```python
for q in earthquakes["features"]:
    print(q["properties"].keys())
```

Take a look at the keys, and see if you can find any likely to
represent earthquake magnitude or location.  Adapt the above prints so
that instead of printing keys in the dictionary, it prints either the
magnitudes or the locations (`print(q["properties"]["????"])`).

# Questions About the Lecture?

Please ask below.

