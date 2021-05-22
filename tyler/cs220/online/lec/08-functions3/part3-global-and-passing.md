# Watch (Part 3)

IFRAME

# Practice

Run the following code (noting any errors), which has two bugs related to local/global variables:

```python
count = 0

def increment():
    count += 1
    print("now at", count)

def reset():
    print("resetting!")
    count = 0

increment()
increment()
increment()
reset()
increment()
increment()
increment()
```

Now fix the functions so that this is printed:
```
now at 1
now at 2
now at 3
resetting
now at 1
now at 2
now at 3
```

Note that first bug resulted in an error (`UnboundLocalError: local
variable 'count' referenced before assignment`), but the bug in
`reset` did not.  The wrong output was printed, but unless you knew
what was expected for the output, it would not have been obvious there
was a problem.  These are called *symantic errors*, and they are the
trickiest to catch and fix.

# Questions About the Lecture?

Please ask below.

