def f(items):
  items.append("!!!")
  print("f:", items)

words = ['hello', 'world']
f(words)
print("after:", words)
