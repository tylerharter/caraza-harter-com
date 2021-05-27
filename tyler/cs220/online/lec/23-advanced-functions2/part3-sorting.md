# Watch (Part 3)

IFRAME

# Practice

Paste the following:

```python
growth = [
    {"name": "A", 2020: 5, 2021: 8},
    {"name": "B", 2020: 3, 2021: 7},
    {"name": "C", 2020: 2, 2021: 3},
]

Write a function that takes a dictionary as a parameter and returns
the ratio of the 2021 value to the 2020 value.  For example, calling
it on `growth[0]` should return 1.6.  Add a print (something like
`print("here")`) inside the function so it will be easy to see
whenever it is called (this becomes less obvious in code that uses
function references).

Now complete the following, replacing `????` with a reference to your
function (remember, to pass a reference, don't put `()` after the
function name, otherwise it will get called, and you'll pass to sort
whatever the function returned, instead of a reference to the function
itself).

```python
growth.sort(key=????, reverse=True)
growth
```

Expected output:

```
[{'name': 'B', 2020: 3, 2021: 7},
 {'name': 'A', 2020: 5, 2021: 8},
 {'name': 'C', 2020: 2, 2021: 3}]
```

# Questions About the Lecture?

Please ask below.

