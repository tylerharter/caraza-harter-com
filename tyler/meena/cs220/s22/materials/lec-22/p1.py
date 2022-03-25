def pretty_print(bullets, indent=0):
    for x in bullets:
        if type(x) == list:
            pretty_print(x, indent+2)
        else:
            print(" "*indent + "*" + x)

values = [
    "Study Tips",
    [
        "use Python Tutor",
        ["go slow", "refine your mental model"],
        "write a lot of code",
        ["run it often", "debug with prints"],
    ]
]
pretty_print(values)
