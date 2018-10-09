def median(nums):
    nums.sort()
    size = len(nums)
    mid = size // 2
    if size % 2 != 0:
        return nums[mid]
    else:
        return (nums[mid - 1] + nums[mid])/2


scores = [2, 4, 3, 5, 1]
print(scores)
print('median =', median(scores))
scores.append(6)
print(scores)
print('median =', median(scores))
