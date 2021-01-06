import time
import beeper

start = int(input("How many seconds? "))

# count down from start to 0

remaining = start
while remaining >= 1:
    print(remaining, "seconds left")
    remaining -= 1
    time.sleep(1)

beeper.beep(10)
