def f(items):
  items = items + ["!!!"]
  print("f:", items)

words = ['hello', 'world']
f(words)
print("after:", words)