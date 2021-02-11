# Trees 2

## 1. Graph Design

### Watch: [19-minute video](https://youtu.be/Noewt4vYGtA)

## 2. BST Search

### Watch: [21-minute video](https://youtu.be/485JOga2SFs)

## 3. BST Dictionary

### Watch: [10-minute video](https://youtu.be/_kB6yBtqy9c)

### Practice

Copy/paste the following, then fix the code so that it is possible to
update values (as noted below, `tree["B"] = 4` doesn't work as it
should).

```python
from graphviz import Graph, Digraph

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    def draw_edges(self, g):
        g.node(self.key, f"{self.key}: {self.val}")

        if self.left != None:
            g.edge(self.key, self.left.key, label="L")
            self.left.draw_edges(g)
            
        if self.right != None:
            g.edge(self.key, self.right.key, label="R")
            self.right.draw_edges(g)

    def _repr_svg_(self):
        g = Digraph()
        self.draw_edges(g)
        return g._repr_svg_()
    
    def __getitem__(self, key):
        if self.key == key:
            return self.val
        elif key < self.key:
            if self.left != None:
                return self.left.__getitem__(key)
        else:
            # self.key > key must be true
            if self.right != None:
                return self.right.__getitem__(key)
            
        return None

    def __setitem__(self, key, val):
        if key < self.key:
            # add it to left subtree
            if self.left == None:
                self.left = Node(key, val)
            else:
                self.left.__setitem__(key, val)
        elif key > self.key:
            # add it to right subtree
            if self.right == None:
                self.right = Node(key, val)
            else:
                self.right.__setitem__(key, val)
                
tree = Node("A", 1)
tree["B"] = 2
tree["C"] = 3
print(tree["A"], tree["B"], tree["C"])

tree["B"] = 4 # TODO: fix __setitem__ so that this works!
print(tree["A"], tree["B"], tree["C"]) # should be 1 4 3
```
