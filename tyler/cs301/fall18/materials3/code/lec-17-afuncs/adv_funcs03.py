def map(f, items):
    result = []
    for item in items:
        new_item = f(item)
        result.append(new_item)
    return result


print(map(abs, [-1, 0, 1]))
print(map(round, [1.23, 3.14]))