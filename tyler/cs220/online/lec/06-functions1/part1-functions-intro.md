# Watch (Part 1)

IFRAME

# Practice

Complete the following so that it correctly identifies whether the
value in x is a number (meaning it is either an int or a float).  Your
code needs to work even if `x = 123` is replaced with something like
`x = True` or `x = "hi"`.

```python
x = 123
x_is_a_num = ????
print("it is", x_is_a_num, "that ", x, " is a number")
```

<details>
    <summary><b>ANSWER</b></summary>
```python
x = 123
x_is_a_num = (type(x) == int) or (type(x) == float)
print("it is", x_is_a_num, "that ", x, " is a number")
```
</details>

# Questions About the Lecture?

Please ask below.

