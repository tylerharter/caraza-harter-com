word = "banana"
counts = {}

for letter in word:
    if letter in counts:
        counts[letter] += 1
    else:
        counts[letter] = 1

print(counts)
