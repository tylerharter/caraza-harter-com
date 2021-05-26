# Watch (Part 2)

IFRAME

# Practice

```python
import copy

def modify(orig):
    nested = ????
    nested[0] = 999     # modify 1 level deep
    nested[1][0] = 333  # modify 2 levels deep

values = [[1, 2], [3, 4]]
modify(values)
print(values)
```

Try replacing `????` with different kinds of copy to end up with different outputs:

* `[[1, 2], [3, 4]]`
* `[[1, 2], [333, 4]]`
* `[999, [333, 4]]`

# Questions About the Lecture?

Please ask below.
