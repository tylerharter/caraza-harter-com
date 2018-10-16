words = ['apple', 'mango', 'orange', 'orange', 'apple', 'mango', 'orange', 'mango', 'orange', 'pineapple', 'avocado']

word_count = dict()

for word in words:
    if word not in word_count:
        word_count[word] = 1
    else:
        word_count[word] += 1

print(word_count)

for key in word_count:
    print(key, ":", word_count[key])

