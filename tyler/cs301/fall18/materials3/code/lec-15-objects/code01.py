def func(s, nums):
    s = s * 2
    nums.append(-1)
    print('s =', s)
    print('nums =', nums)


word = "hi"
items = [1, 2, 3]
print('word =', word)
print('items =', items)
func(word, items)
print('word =', word)
print('items =', items)
