total = 0
count = 0

while True:
    x = input("enter an x [0-100], or q [quit]: ") # x is a str
    
    if x == "q":
        break # all done, user wants to exit
    
    x = float(x) # after this, x is a float

    if x < 0 or x > 100:
        print("out of range!")
        continue # give another try with better numbers

    total += x
    count += 1

    print("avg:", total/count)

    # TODO: figure out when to break out of here
