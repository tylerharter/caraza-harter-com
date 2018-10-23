suffix = {1: "st", 2:"nd", 3:"rd"}

for num in range(10):
    print(str(num) + suffix.get(num, "th"))
