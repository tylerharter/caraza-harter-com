# Regular Expressions 2

## 1. Email Regex Practice (Part 1)

### Watch: [21-minute video](https://youtu.be/DPuIJHsd6O0)

### Practice: More Emails

Below is slightly modified version of the example from lecture.

```python
import re, requests

r = requests.get(????)
s = ????

suffix = r"\.(edu|com|org)"
at = r"(@|[aA][tT])"
opt_brackets = r"[\(\)\{\}\[\]]?"
email = r"(\w+)\s*" + opt_brackets + at + opt_brackets + r"\s*(\w+)" + suffix
for match in re.findall("("+email+")", s):
    print(match[1]+"@"+match[3]+"."+match[4])
```

Complete the code so that it grabs the three emails from this page: https://tyler.caraza-harter.com/cs320/f20/hidden.html

Review the requests module as necessary: https://requests.readthedocs.io/en/master/user/quickstart/#response-content

## 2. Function Name Regex Practice (Part 2)

### Watch: [20-minute video](https://youtu.be/1_GzP8sjhOM)
