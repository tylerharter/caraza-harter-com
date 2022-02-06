def func_c():
   print("C")

def func_b():
   print("B1")
   func_c()
   print("B2")

def func_a():
   print("A1")
   func_b()
   print("A2")

func_a()
