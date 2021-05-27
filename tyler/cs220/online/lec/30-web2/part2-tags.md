# Watch (Part 2)

IFRAME

# Practice

The main way to see HTML rendered is to write it in a .html file, then
open that .html file in a browser.

Alternatively, if you're in Jupyter, you can fill a string with the
HTML contents (tags, text, etc.), then call the `HTML(...)` function
to see it.

Try it:

```python
from IPython.display import HTML
HTML("<h1>Hello, Wold!</h1>")
```

Complete the following function, which use the `HTML(...)` function,
to visualize a Python list as a bulleted HTML list (`<ul>`).

```python
def viz_list(items):
    html_str = ????
    for item in items:
        html_str += ????
    html_str += "</ul>"
    return HTML(html_str)

viz_list(["apple", "banana", "carrot"])
```

# Questions About the Lecture?

Please ask below.

