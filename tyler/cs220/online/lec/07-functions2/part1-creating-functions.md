# Watch (Part 1)

IFRAME

# Practice

Paste and run the following:

```python
def get_email(user, domain):
    return user + "@" + domain

print(get_email("test", "gmail.com"))
print(get_email("example", "outlook.com"))
print(get_email("morteza", "wisc.edu"))
```

Now, let's say we want to be able to call `get_email` without
specifying a domain, and have it default to wisc.edu, like this:

```python
print(get_email("chancellor"))
```

Modify the function definition line (`def get_email(user, domain):`)
to have a default argument for `domain`.  It should be possible to
call the function like ealier with two arguments, or with one argument
(having domain default to "wisc.edu").

# Questions About the Lecture?

Please ask below.

