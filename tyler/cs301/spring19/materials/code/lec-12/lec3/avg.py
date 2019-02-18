total = 0
count = 0

while True:
    val = input("enter a percent [q for exit]:")
    if val == "q":
        break

    val = int(val)
    if not (0 <= val <= 100):
        print("yikes!  not in range")
        continue
    total += val   
    count += 1
    print("AVG", total/count)
