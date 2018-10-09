def add_nums(nums):
    print("nums is", nums)
    tot = 0
    for x in nums:
        print(x)
        tot += x
    return tot

L = [1, 2, 3]
print("L is", L)
total = add_nums(L)
print("TOTAL:", total)