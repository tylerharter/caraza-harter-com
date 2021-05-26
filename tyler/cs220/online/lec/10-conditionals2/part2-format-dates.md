# Watch (Part 2)

IFRAME

# Practice

Complete the below function to convert a 24-hour formatted time to
12-hour formatted time.  0:00 is 12am and 12:00 is 12pm.  Otherwise,
hours less than 12 just get an "am" added to the end, and numbers over
12 get 12 subtracted away, before "pm" gets added.

```python
def convert_24_to_12(????):
   if orig == 0:
       result = "12am"
   elif orig == 12:
       return "12pm"
   elif ????:
       result = str(orig) + "am"
   else:
       result = ????
   ????

def convert_24_to_12(orig):
   if orig == 0:
       result = "12am"
   elif orig == 12:
       return "12pm"
   elif orig < 12:
       result = str(orig) + "am"
   else:
       result = str(orig-12) + "pm"
   return result

print(convert_24_to_12(0))   # expected 12am
print(convert_24_to_12(1))   # expected 1am
print(convert_24_to_12(11))  # expected 11am
print(convert_24_to_12(12))  # expected 12pm
print(convert_24_to_12(13))  # expected 1pm
print(convert_24_to_12(19))  # expected 7pm
print(convert_24_to_12(23))  # expected 11pm
```

# Questions About the Lecture?

Please ask below.

