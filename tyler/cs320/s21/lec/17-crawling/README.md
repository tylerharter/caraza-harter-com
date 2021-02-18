# Web Crawling

## 1. More Selenium

### Watch: [21-minute video](https://youtu.be/ZUvGvFo4o4Y)

## 2. BFS for Web

### Watch: [29-minute video](https://youtu.be/8wjQTweW_uQ)

### Practice: Start Node

Copy+paste the demo code from lecture:

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

start_url = "https://tyler.caraza-harter.com/cs320/s21/lec/17-crawling/practice1/1.html"
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

1. update the code: try starting from node 1 in practice example 3 `start_url = "https://tyler.caraza-harter.com/cs320/s21/lec/17-crawling/practice3/1.html"`

2. if you want to discover all the nodes, are some places better to start than others?  Would it be better to start in node 1 or 4?

3. replace `1.html` with `4.html` to check your intuition about which is a better starting point
