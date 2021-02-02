# Recursion

## 1. Recursion

### Watch: [14-minute video](https://youtu.be/vU2eu7HJbSQ)

## 2. Nested Lists

### Watch: [19-minute video](https://youtu.be/GbX1pDMSZj4)

### Practice: recursive sum

Complete a function that adds all the integers in a structure of nested lists:

```python
def rec_sum(L):
    total = 0
    for x in L:
        if ????: # is x a sub list?
            ???? # get sum from sub list, add to our total
        else:
            total += x
    return total

rec_sum([1,2,[[3],4]]) # should be 10
```

<details>
    <summary>ANSWER</summary>
    <p>
    <b>isinstance(x, list)</b> and <b>total += rec_sum(x)</b>
    </p>
</details>

## 3. Linked Lists

### Watch: [14-minute video](https://youtu.be/vaHpN5AszdI)
