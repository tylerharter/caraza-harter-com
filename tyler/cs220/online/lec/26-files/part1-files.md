# Watch (Part 1)

IFRAME

# Practice

Complete the following two functions.  `greetings` should print a
hello message, using the users name (if specified in a file named
"name.txt").  You need to check whether the file exists, and if so,
read it in.

The `set_name` function updates the name in the name.txt file.  You
need to pass a second argument when opening the file so that it is
writable.

Specify your name for the call to `set_name` at the end.

```python
import os

def greetings():
    name = "unknown"
    if os.path.????("name.txt"):
        f = open("name.txt")
        name = f.????()
        f.close()
    print("Hello", name)

def set_name(name):
    f = open("name.txt", ????)
    f.write(name)
    f.close()
    
greetings()
set_name(????)
greetings()
```

Run the program (in a .py or .ipynb).  Then restart and run again.
Note that the name is remembered from the first time the program ran.

# Questions About the Lecture?

Please ask below.

