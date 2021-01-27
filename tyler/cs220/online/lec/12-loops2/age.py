# keep asking for ages
# print the average
# exit when user types "q"
# ignore unreasonable numbers

total = 0
count = 0

while True:
    age = input("Enter an age: ")
    if age == "q":
        break # are we done?
    age = int(age)
    if age > 150 or age < 0:
        print("bad age")
        continue # skip bad input?
    total += age
    count += 1
    
    avg = total/count
    print("AVG:", avg)