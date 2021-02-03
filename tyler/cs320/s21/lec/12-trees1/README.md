# Sep 30 Lecture

## 1. Words to Describe Graphs

### Watch: [14-minute video](https://youtu.be/TeOHjYaIurY)

## 2. Tree Recursion

### Watch: [14-minute video](https://youtu.be/UeRV7Zx3GAE)

### Practice

Copy/paste the following to a cell, and complete so that `count_nodes`
returns the total number of nodes in the tree:

```python
from graphviz import Graph, Digraph

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def draw_edges(self, g):
        if self.left != None:
            g.edge(self.val, self.left.val, label="L")
            self.left.draw_edges(g)

        if self.right != None:
            g.edge(self.val, self.right.val, label="R")
            self.right.draw_edges(g)

    def _repr_svg_(self):
        g = Digraph()
        self.draw_edges(g)
        return g._repr_svg_()

    def count_nodes(self):
        count = 1
        # how many descendants on the left?
        if self.left != None:
            ????
        # how many descendants on the right?
        if ?????:
            count += self.right.count_nodes()
        return count

root = Node("A")
root.left = Node("B")
root.right = Node("C")
root.left.right = Node("D")
root.count_nodes()
```

## 3. Tree Search

### Watch: [21-minute video](https://youtu.be/e5anHRCcRmw)
