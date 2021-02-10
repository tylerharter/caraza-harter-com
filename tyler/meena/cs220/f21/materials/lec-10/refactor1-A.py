def or2(cond1, cond2):
    rv = False
    rv = rv or cond1
    rv = rv or cond2
    return rv

print(or2(False, True))
