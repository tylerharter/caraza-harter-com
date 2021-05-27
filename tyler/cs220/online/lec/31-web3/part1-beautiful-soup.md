# Watch (Part 1)

IFRAME

# Practice

Run this:

```python
html = '''
Schools:
<a href="https://umich.edu/">Michigan</a>,
<b><a href="https://www.wisc.edu">Wisconsin</a></b>,
<a href="https://twin-cities.umn.edu/">Minnesota</a>
'''
HTML(html)
```

Complete the following code to extract the hyperlink from the a tag that's inside a bold tag:

```python
from bs4 import BeautifulSoup
doc = BeautifulSoup(html, "html.parser")
doc.find(????).find(????).attrs[????]
```

# Questions About the Lecture?

Please ask below.

