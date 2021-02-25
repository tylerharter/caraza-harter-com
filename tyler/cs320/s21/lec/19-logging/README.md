# Logging

## 1. Logging

### Watch: [27-minute video](https://youtu.be/2NWBdEQnwIg)

### Practice:

Add a subtract function and decorate it with `trace`:

```python
def trace(fn):
    def wrapper(*args):
        result = fn(*args)
        arg_str = ", ".join([repr(a) for a in args])
        print(f"{fn.__name__}({arg_str}) -> {result}")
        return result

    return wrapper

@trace
def absolute(x):
    if x < 0:
        x *= -1
    return x

@trace
def add(x, y):
    return x * y # hmmmm????

print(absolute(-3))
print(add(2, 2))
print(add(3, 4))
```

## 2. Rate Limiting

### Watch: [15-minute video](https://youtu.be/DwqjzPfL2MA)

## 3. robots.txt

### Watch: [7-minute video](https://youtu.be/TNH19pGVna4)

### Practice:

Copy+paste the BFS crawler we introduced in an earlier lecture:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from IPython.core.display import display, Image
from graphviz import Digraph
from collections import deque

options = Options()
options.headless = True
b = webdriver.Chrome(options=options)
b.set_window_size(300, 200)

# take URL to visit
# return other URLs based on the links
# show a screenshot of the page
def visit_page(url):
    b.get(url)
    b.save_screenshot("screen.png")
    display(Image("screen.png"))
    
    links = b.find_elements_by_tag_name("a")
    return [link.get_attribute("href") for link in links]

def node_name(url):
    return url.split("/")[-1].split(".")[0]

start_url = "https://tyler.caraza-harter.com/cs320/f20/lectures/lec-17/practice1/1.html"
todo = deque([start_url])
added = set(todo)

gv = Digraph(engine="neato") # _repr_svg_

def visit_next():
    # 1. do the first thing on the list
    url = todo.popleft()
    gv.node(node_name(url))

    children_urls = visit_page(url)
    
    # 2. add new things to the end of the list
    for child_url in children_urls:
        if not child_url in added:
            todo.append(child_url)
            added.add(child_url)
        gv.edge(node_name(url), node_name(child_url))
    display(gv)
    print(todo)

while len(todo) > 0:
    visit_next()
```

Change the `start_url` to
`https://tyler.caraza-harter.com/cs320/f20/lectures/lec-17/calendar/A.html`.
Notice a problem?  Might need to do a Kernel Restart here (sorry!).

Let's not explore nodes we're not allowed to.  Add this near the top of the code:

```python
import urllib.robotparser
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://tyler.caraza-harter.com/robots.txt")
rp.read()
```

Then, when looping over children, skip ones blocked by robots.txt:

```python
        if not rp.can_fetch("cs320robot", child_url):
            continue
```