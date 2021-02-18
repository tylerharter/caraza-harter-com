# Flask

## 1. Internet Overview

### Watch: [19-minute video](https://youtu.be/vIaNwi2w894)

## 2. Complex Pages

### Watch: [9-minute video](https://youtu.be/ClrrFAxB_hk)

## 3. Flask

### Watch: [15-minute video](https://youtu.be/s5r72kMY4Bc)

### Practice:

Let's create a page that shows a simple graph.  Complete the following in a file named `app.py`:

```python
import os, sys, json
import pandas as pd
from flask import Flask
from graphviz import Graph

app = Flask(__name__)

@app.route(????)
def rand_plot():
    g = Graph()
    g.edge("a", "b")
    g.edge("b", "c")
    g.edge("c", "a")
    return g.????()

if __name__ == '__main__':
    app.run("0.0.0.0", "54321")
```

Requests to "/graph.svg" should show the SVG graph.  Remember that
graphviz graphs have a `_repr_svg_` method!

Run the application on your virtual machine:

```python
python3 app.py
```

In a web browser, go to `http://YOUR_IP_ADDRESS:54321/graph.svg`

## 4. Decorators

### Watch: [6-minute video](https://youtu.be/lqm2aN37KZg)
