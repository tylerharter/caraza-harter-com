# Scoring Classifiers: Does it Work Well?

## 1. Confusion Matrices

### Watch: [14-minute video](https://youtu.be/FYPj2xnv_No)

### Practice: Reading Confusion Matrices

Paste and run the following to quiz yourself:

```python
from IPython.core.display import display
import numpy as np
import pandas as pd
import time

def question_confusion_matrix():
    labels = ["apples", "oranges", "bananas"]
    data = np.random.randint(0, 100, size=(len(labels), len(labels)))
    df = pd.DataFrame(data, index=labels, columns=labels)
    print("Confusion Matrix:")
    display(df)
    i,j = np.random.randint(0, len(labels), size=2)
    answer = input(f"How many {labels[i]} are classified as {labels[j]}?  ")
    correct = df.iloc[i,j]
    if int(answer) == correct:
        print("Good job!")
        return True
    else:
        print("!"*40)
        print(f"Actually, the answer is {correct}")
        print("!"*40)
        time.sleep(2.5)
        return False

def question_binary_class(i=0):
    names = ["True Negatives", "False Positives", "False Negatives", "True Positives"]
    data = np.random.randint(0, 100, 4)
    df = pd.DataFrame(data.reshape(2,2), index=[False, True], columns=[False, True])
    print("Confusion Matrix:")
    display(df)
    answer = input(f"How many {names[i]} are there?  ")
    correct = data[i]
    if int(answer) == correct:
        print("Good job!")
        return True
    else:
        print("!"*40)
        print(f"Actually, the answer is {correct}")
        print("!"*40)
        time.sleep(2.5)
        return False
    
score = 0

for i in range(3):
    score += int(question_confusion_matrix())
    print("\n")

questions = np.arange(4)
np.random.shuffle(questions)
for i in questions:
    score += int(question_binary_class(i))
    print("\n")

print(f"You got {score} of 7 correct.")
```

## 2. Recall and Precision

### Watch: [14-minute video](https://youtu.be/HuEtoZ5U1e0)

### Practice: Recall and Precision

Paste and run the following to test yourself.

Remember to put the value from the diagonal in the numerator and
either the sum of the row (recall) or sum of the column (precision) in
the denominator.

These functions make sure the denominator is always either 10 or 20,
to help you do the math in your head.

```python
def question_recall():
    labels = ["apples", "oranges", "bananas"]
    data = np.random.randint(0, 6, size=(len(labels), len(labels)))
    i = np.random.randint(0, len(labels))
    data[i,i] = 0
    data[i,i] = 10 - data[i,:].sum()
    data *= np.random.randint(1,3)
    df = pd.DataFrame(data, index=labels, columns=labels)
    print("Confusion Matrix:")
    display(df)    
    answer = input(f"What is the recall for {labels[i]}?  ")
    correct = (data[i,i] / data[i,:].sum()).round(1)
    if float(answer) == correct:
        print("Good job!")
        return True
    else:
        print("!"*40)
        print(f"Actually, the answer is {correct}")
        print("!"*40)
        time.sleep(2.5)
        return False
    
def question_precision():
    labels = ["apples", "oranges", "bananas"]
    data = np.random.randint(0, 6, size=(len(labels), len(labels)))
    i = np.random.randint(0, len(labels))
    data[i,i] = 0
    data[i,i] = 10 - data[:,i].sum()
    data *= np.random.randint(1,3)
    df = pd.DataFrame(data, index=labels, columns=labels)
    print("Confusion Matrix:")
    display(df)
    answer = input(f"What is the precision for {labels[i]}?  ")
    correct = (data[i,i] / data[:,i].sum()).round(1)
    if float(answer) == correct:
        print("Good job!")
        return True
    else:
        print("!"*40)
        print(f"Actually, the answer is {correct}")
        print("!"*40)
        time.sleep(2.5)
        return False

score = 0

for i in range(3):
    score += int(question_recall())
    print("\n")
    score += int(question_precision())
    print("\n")

print(f"You got {score} of 6 correct.")
```

## 3. Regularization and Standardization

### Watch: [16-minute video](https://youtu.be/Kc6Jsph1kyM)
