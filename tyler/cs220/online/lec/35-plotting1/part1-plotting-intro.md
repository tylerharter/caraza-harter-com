# Watch (Part 1)

IFRAME

# Practice

Lets create a bar plot to show the frequency that each letter appears
in the sentence "The quick brown fox jumps over the lazy dog".

First, create a pandas Series where each entry the the upper case
version of a letter in the above string.  You'll want to use
`.replace(" ", "")` to get rid of spaces, `.upper()` to make
everything uppercase, and `list(...)` to covert the string to a list
of characters, from which a Series can be created.

```
import pandas as pd
text = "The quick brown fox jumps over the lazy dog"
letters = pd.Series(????)
letters
```

Expected:

```
0     T
1     H
2     E
3     Q
4     U
5     I
6     C
7     K
8     B
9     R
10    O
11    W
12    N
13    F
14    O
15    X
...
```

Use this
(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html)
on `letters` to count how often each letter appears:

```python
counts = ????
counts
```

Expected:

```
O    4
E    3
T    2
R    2
U    2
H    2
Q    1
L    1
...
```

Create a bar plot plot from the `counts` Series:

```python
ax = ????.plot.????()
ax.set_xlabel("Letter")
ax.????("Frequency")
```

# Questions About the Lecture?

Please ask below.

