x = input("enter x: ")
y = input("enter y: ")
x = float(x)
y = float(y)
print("the sum is", x + y, sep=" ")
# same as:
# print("the sum is", x + y)

print("the sum is", x + y, sep=": ", end=".\n")
print("thanks for summing numbers")
