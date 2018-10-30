def pretty(bullets, indent=0):
    for b in bullets:
        if type(b) == list:
            pretty(b, indent+2)
        else:
            print(' '*indent + b)

bullets = ["A", "B", ["1", "2"],
           "C", ["1", ["i", "ii"]]]
pretty(bullets)
