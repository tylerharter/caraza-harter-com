# Graph Search 1

## 1. Review BSTs (Binary Search Trees)

### Watch: [11-minute video](https://youtu.be/5QsNVVxe3OE)

## 2. DFS (Depth-First Search)

### Watch: [27-minute video](https://youtu.be/HbjA92cfFYE)

### Practice: `is_connected`

Copy/paste the following example from lecture, then complete the new
`is_connected` method.  The method should return True if the graph is
connected, meaning there's a path between any given pair of nodes.
The method should return False if the `find` method cannot find a path
for some pair of nodes.

```python
from graphviz import Graph, Digraph

class mygraph:
    def __init__(self):
        # name => Node
        self.nodes = {}
        self.visited = set()
    
    def node(self, name):
        node = Node(name)
        self.nodes[name] = node
        node.graph = self
    
    def edge(self, src, dst):
        # automatically add missing nodes
        for name in [src, dst]:
            if not name in self.nodes:
                self.node(name)
        self.nodes[src].children.append(self.nodes[dst])
        
    def _repr_svg_(self):
        # draw nodes+edges, non-recursively!
        g = Digraph()
        for n in self.nodes:
            g.node(n)
            for child in self.nodes[n].children:
                g.edge(n, child.name)
        return g._repr_svg_()
    
    def find(self, src, dst):
        self.visited = set()
        return self.nodes[src].find(self.nodes[dst])
    
    def is_connected(self):
        for src in self.nodes.keys():
            for dst in ????:
                if self.find(src, dst) == ????:
                    return False
        return ????

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.graph = None # back reference

    def __repr__(self):
        return self.name

    def find(self, dst):
        if self in self.graph.visited:
            return None
        self.graph.visited.add(self)
        
        if self == dst:
            return (self,)

        for child in self.children:
            childpath = child.find(dst)
            if childpath != None:
                return (self,) + childpath

        return None

g = mygraph()
g.edge("A", "B")
g.edge("A", "C")
g.edge("B", "D")
g.edge("B", "E")
g.edge("C", "F")
g.edge("C", "G")
g.edge("F", "C")
g.edge("G", "A")
g.edge("D", "E")
g.edge("E", "D")
g.edge("B", "C")
print(g.is_connected())
g
```

The above graph is not connected, so your method should return False.
Add one more edge so that it is connected, then make sure your method
returns True for the new graph.

## 3. BFS (Breadth-First Search)

### Watch: [11-minute video](https://youtu.be/WHgSMapnrzk)
