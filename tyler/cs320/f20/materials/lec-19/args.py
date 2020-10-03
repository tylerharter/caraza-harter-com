def format(template, *args):
    parts = template.split("{}")
    assert(len(parts) == len(args) + 1)
    result = []
    for i in range(len(args)):
        result.append(parts[i])
        result.append(args[i])
    result.append(parts[-1])
    return "".join(result)

s = "Dear {}, you are invited to {}."

print(format(s, "Student", "hackathon"))
