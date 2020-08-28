def fix(moves, should):
    if moves and not should:
        return "duct tape"
    elif not moves and should:
        return "WD-40"
    elif moves and should:
        return "good"
    elif not moves and not should:
        return "good"

print(fix(False, False))
