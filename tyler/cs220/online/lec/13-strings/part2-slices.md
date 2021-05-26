# Watch (Part 2)

IFRAME

# Practice

The `find` method gives the index of one string within another string.
Slicing is based on indexes, and there are many use cases where `find`
is used to calculate those indexes.

For example, the following code snippet extracts the text surrounding
(1 character before and 1 after) the first "*" character:

```python
text = "ABCDEFG*HIJK*LMN*OPQRSTUVWXYZ"
first_star = text.find("*")
text[first_star-1 : first_star+2]
```

Complete the following function to extract the text inside the first
pair of parentheses in a string:

```python
def parentheses_extractor(s):
    open_idx = ????
    close_idx = ????
    return s[???? : ????]

parentheses_extractor("ABCD(EFG)HIJKLMNOPQRSTUVWXYZ") # should return "EFG"
```

# Questions About the Lecture?

Please ask below.

