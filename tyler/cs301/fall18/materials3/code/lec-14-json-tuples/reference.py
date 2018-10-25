
def func(x):
    x += 1
    print('x =', x)

def func2(nums):
    nums[0] = -1

x = 42
print('x =', x)
func(x)
print('x =', x)

nums = [1, 2, 3]
print('nums: ', nums)
func2(nums)
print('nums: ', nums)