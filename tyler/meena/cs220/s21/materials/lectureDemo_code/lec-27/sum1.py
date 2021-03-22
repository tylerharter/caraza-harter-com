f = open('nums.txt')
nums = list(f)

total = 0
for x in nums:
    total += x

print(total)
