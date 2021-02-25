# A/B Testing

## 1. A/B Testing (Part 1)

### Watch: [17-minute video](https://youtu.be/Hp2ExNB243I)

### Practice: Contingency Table

Suppose version A of a button was shown 100 times, and users clicked
it half of those times.  An alternative, B, was also shown to users;
they clicked it 7 times and didn't click it 3 times.

70% feels better that 50%, but is it a significant difference, given
the small sample for B?  Complete the following to find out:

```python
import pandas as pd
from scipy import stats

df = pd.DataFrame({
    "click":    {"A": 50, "B": ????},
    "no-click": {"A": 50, "B": ????},
})

print(df)

_, pvalue = stats.fisher_exact(df)
if pvalue < 0.05:
    a_ratio = df.loc["A", "click"] / df.loc["A", "no-click"]
    b_ratio = ????
    if a_ratio > b_ratio:
        print("A is better")
    else:
        print("B is better")
else:
    print("no significant difference")
df
```

What about if we still got 70% clicks on B out of a smaple of 40 (28
clicks and 12 no clicks)?  Modify the code and find out.

## 2. A/B Testing (Part 2)

### Watch: [24-minute video](https://youtu.be/TnJytrxUmWY)
