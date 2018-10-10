def censor(orig):
    dirty = ["midterm", "darn", "omg"]

    words = orig.split()
    cleaned = []

    for w in words:
        if w.lower() in dirty:
            cleaned.append("*" * len(w))
        else:
            cleaned.append(w)

    return " ".join(cleaned)


s = 'OMG this CS 301 class is awesome'
print("DIRTY:", s)
print("CLEANED:", censor(s))
