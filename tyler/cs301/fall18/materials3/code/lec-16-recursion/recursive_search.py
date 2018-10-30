# Goal: does a given number exist in a recursive structure?
# Input:
# - A number
# - A list of numbers and lists (which contain other numbers and lists)
# Output:
# - True if there’s a list containing the number, else False
# 
# Example:
# >>> contains(3, [1,2,[4,[[3],[8,9]],5,6]])
# True
# >>> contains(12, [1,2,[4,[[3],[8,9]],5,6]])
# False

#Recursively search for an item in a nested list.
def contains(key, nums):
    for item in nums:
        if type(item) == list:
            if contains(key, item):
                return True
        elif key == item:
            return True
    return False


my_nums = [1, 2, [4, [[3], [8, 9]], 5, 6]]
print(contains(3, my_nums))

