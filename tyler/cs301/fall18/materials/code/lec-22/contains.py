def contains(target, nums):
    for item in nums:
        if type(item) == list:
            if contains(target, item):
                return True
        elif item == target:
            return True
    return False

print(contains(2, [1, [2, 3]]))
