# Watch (Part 2)

IFRAME

# Practice

Copy/paste the following code and run it (in Jupyter or PythonTutor)
to compute WI sales tax (5%) over the purchase of four computer
components:

```python
motherboard = 125
cpu = 300
ram = 100
ssd = 220
tax = 0
tax += 0.05 * motherboard
tax += 0.05 * cpu
tax += 0.05 * ram
tax += 0.05 * ssd
print("TOTAL TAX", tax)
```

Notice how 0.05 is repeated above.  Such repetition is usually a red
flag when you're programming.  If the sales tax changes to 5.5%, four
lines of code will need to change instead of one.

Adapt the above code so that there is a `tax_rate` variable equal 0.05
and use that on the four lines that add to tax.  Make sure your code
produces the same result as before, then try changing the tax rate to
5.5% (by modifying a single line!) to see what the new sales tax is.

<details>
    <summary><b>ANSWER</b></summary>
```python
motherboard = 125
cpu = 300
ram = 100
ssd = 220
tax_rate = 0.055
tax = 0
tax += tax_rate * motherboard
tax += tax_rate * cpu
tax += tax_rate * ram
tax += tax_rate * ssd
print("TOTAL TAX", tax_rate)
```
</details>

# Questions About the Lecture?

Please ask below.

