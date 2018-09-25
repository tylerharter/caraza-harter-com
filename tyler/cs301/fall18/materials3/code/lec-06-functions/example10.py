# function variables do not persist between calls
def count():
    x = 1
    x += 1  # NOTE: += is a short form for saying x = x + 1
    print(x)


count()
count()
count()

# LESSON 3: variables start fresh
# every time a function is called again
