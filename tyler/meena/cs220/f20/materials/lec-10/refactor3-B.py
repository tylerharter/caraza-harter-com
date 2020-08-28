def fix(moves, should):
    if should:
        if moves:
            return "duct tape"
        else:
            return "good"
    else:
        if moves:
            return "good"
        else:
            return "duct tape"

print(fix(False, False))
