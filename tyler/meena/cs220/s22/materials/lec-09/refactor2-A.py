def and2(cond1, cond2):
    rv = False
    rv = rv and cond1
    rv = rv and cond2
    return rv

print(and2(True, True))
