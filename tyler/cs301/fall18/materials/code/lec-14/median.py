def median(nums):
    nums.sort()
    print('SORTED', nums)

    n = len(nums)

    if n % 2 == 1:
        # for odd numbers
        return nums[(n-1) // 2]
    else:
        # it must be even
        m1 = nums[(n-1) // 2]
        m2 = nums[(n-1) // 2 + 1]
        return (m1+m2) / 2

lst = [9001.1, 9002.2, 9003.3, 100.4, 300.5, 50.6, 1000.7]
m = median(lst)
print(m)