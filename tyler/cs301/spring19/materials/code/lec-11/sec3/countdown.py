import time
import beeper

seconds = input("how many seconds [q for quit]? ")

while seconds != "q":
    seconds = int(seconds)

    while seconds > 0:
        print(seconds, "remaining")
        time.sleep(1)
        seconds -= 1
                
    print("beep beep beep")
    #beeper.beep(3)
    seconds = input("how many seconds [q for quit]? ")
