names = [
    ("Cindy", "Baker"),
    ("Alice", "Clark"),
    ("Bob", "Adams"),
]

def extract(name_tuple):
    return name_tuple[1]

last_names = list(map(extract, names))
print('last_names =', last_names)

names.sort(key=extract)

print(names)