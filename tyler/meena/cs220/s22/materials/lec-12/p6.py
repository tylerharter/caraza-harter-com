call_num = 0

def next():
    global call_num
    call_num += 1
    if call_num == 1:
        return 3
    elif call_num == 2:
        return 2
    elif call_num == 3:
        return 0
    elif call_num == 4:
        return 5
    else:
        return -1

# assume next() returns 3 the first time it is called,
# 2 the 2nd time, 0 (3rd), 5 (4th), and -1 (5th and beyond)
total = 1
while True:
    num = next()
    if num < 0:
        break
    elif num == 0:
        continue
    total *= num
print(total)
