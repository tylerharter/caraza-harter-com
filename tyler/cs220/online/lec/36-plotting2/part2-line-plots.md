# Watch (Part 2)

IFRAME

# Practice

The City of Madison has placed sensors on State St. near the capital
to count pedestrians at various locations.  The data is here:
https://data-cityofmadison.opendata.arcgis.com/datasets/upper-state-street-pedestrian-counts

Paste the following to get a DataFrame describing the average hourly
pedestrians measured by 4 different sensors (columns) across 7 days of
the week:

```python
pedestrians = pd.DataFrame({
  'SS_22_State_St__North_Side': {
  0: 88.67374810318664,
  1: 87.99627976190476,
  2: 102.8030303030303,
  3: 90.48409090909091,
  4: 140.68030303030304,
  5: 172.32440476190476,
  6: 119.20370370370371},
 'SS_23_State_St__South_Side': {
  0: 75.53869499241274,
  1: 77.29613095238095,
  2: 89.3,
  3: 76.90151515151516,
  4: 118.14393939393939,
  5: 153.3251488095238,
  6: 96.29783950617283},
 'F200_State_St____Goodman_s': {
  0: 73.61153262518968,
  1: 75.7671130952381,
  2: 88.55075757575757,
  3: 72.0060606060606,
  4: 113.72954545454546,
  5: 140.6592261904762,
  6: 97.25617283950618},
 'F200_State_St____Art_Center': {
  0: 54.92412746585736,
  1: 60.716517857142854,
  2: 69.63484848484849,
  3: 57.621212121212125,
  4: 86.4060606060606,
  5: 118.36309523809524,
  6: 74.80941358024691}})
pedestrians
```

This plots a line for the first column (one sensor location):

```python
ax = pedestrians["SS_22_State_St__North_Side"].plot.line()
ax.set_xlabel("Day of Week")
ax.set_ylabel("Avg Hourly Pedestrians")
```

Modify the above to plot all four lines (you want to call
`.plot.line()` on the DataFrame directly instead of one column of the
DataFrame).

The numbers correspond to indexes into this list (for example, Monday is 0):

```python
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
```

Use that list to put proper day names in the x-axis:

```python
ax.set_xticks(range(len(????)))
ax.set_xticklabels(????)
```

# Questions About the Lecture?

Please ask below.

