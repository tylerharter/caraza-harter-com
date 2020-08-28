# BAD EXAMPLE: remove odd numbers
nums = [1,3,5,2,4,6]
for x in nums:
    if x % 2 == 1:
        nums.remove(x)
print(nums)
