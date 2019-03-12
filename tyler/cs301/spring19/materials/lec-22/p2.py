def foo(nums):
    nums.append(3)
    print(nums)
items = [1,2]
numbers = items
foo(numbers)
print(items)
print(numbers)