# Classification

## 1. LogisticRegression Classifier (it's not a regressor!)

### Practice: Fit, Score, Predict

Start with the following data:

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.DataFrame(
    columns=["x1", "x2", "x3", "y"],
    data = [
       [5, 1, 2, True],
       [4, 3, 3, False],
       [0, 3, 4, False],
       [0, 1, 4, False],
       [3, 1, 3, False],
       [5, 1, 1, True],
       [6, 3, 1, True],
       [1, 4, 2, False],
       [3, 0, 0, True],
       [7, 1, 0, True],
       [2, 4, 0, False],
       [3, 4, 0, False],
       [3, 5, 1, False],
       [9, 4, 3, True],
       [0, 0, 3, False],
       [7, 0, 4, True],
       [6, 0, 1, True],
       [2, 4, 2, False],
       [5, 3, 0, True],
       [4, 0, 1, True]
    ]
)
df
```

The pattern is that y is True whenever x1 >= x2 + x3.  Let's see how
well a LogisticRegression can learn that pattern.

We pre-shuffled the data before giving it to you, so lets use the
first 10 rows for training and the latter 10 for testing (no need to
use sklearn's `train_test_split`).  Complete the following slices to
do this:

```python
train, test = df.iloc[????], df.iloc[????]
```

<details> <summary>ANSWER</summary> :10, 10: </details>

Fit a classifier to the training data:

```python
lr = LogisticRegression()
lr.fit(????, ????)
```

<details> <summary>ANSWER</summary> train[["x1", "x2", "x3"]], train["y"]</details>

How accurate is the model on the test data?  Copy the last line from
above, then replace "fit" with "score", and replace "train" with
"test".  You should get 0.9.

Let's add the predictions to a column in the test DataFrame (note,
test refers to subset of the rows in df; pandas will complain with
`SettingWithCopyWarning` if we add a column to this subset without
making train a full copy of those rows):

```python
????
test["predicted_y"] = lr.predict(????)
test
```

<details> <summary>ANSWER</summary> test=test.copy(), test[["x1", "x2", "x3"]] </details>

Let's show the rows in the test dataset that the model mis-classifies:

```python
test[test["y"] != ????]
```

<details> <summary>ANSWER</summary> test["predicted_y"] </details>

Note that `fit_intercept=True` is the default for LogisticRegression.
We overrode this default in the lecture video, but not here.  This
means that both `lr.coef_` and `lr.intercept_` will be set.

The formula is very similar to before -- we still do the dot product,
but then add the intercept:

```python
test[["x1", "x2", "x3"]] @ lr.coef_.T + lr.intercept_ > 0
```

Verify that the above calculation produces the same results as we saw
with `lr.predict` earlier.

### Watch: [29-minute video](https://youtu.be/Pao7GkhOCRE)

## 2. Decision Boundaries

### Watch: [15-minute video](https://youtu.be/cWYgtUU9COg)
