# GOOD EXAMPLE: remove odd numbers
nums = [1,3,5,2,4,6]
nums2 = []
for x in nums:
    if x % 2 != 1:
        nums2.append(x)
nums = nums2
print(nums)
