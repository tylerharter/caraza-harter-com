total = 0 # sum
count = 0

while True:
    #Handle "q" input for quitting
    age = input("Enter an age [0-100]: ")
    if age == "q":
        break

    age = float(age)

    if age < 0 or age > 100:
        print("Bad input!")
        continue

    total += age
    count += 1

    print("Average age of user so far is: ", total / count)
    
