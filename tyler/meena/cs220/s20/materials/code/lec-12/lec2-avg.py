total = 0 # sum
count = 0

while True:
    x = float(input("enter an x [0-100]: "))

    if x < 0 or x > 100:
        print("bad input!")
        continue

    total += x
    count += 1

    print("AVG", total/count)
    
