def first(items):
    return items[0]

def smallest(items):
    items = sorted(items)
    return items[0]

numbers	= [4,5,3,2,1]
print("first:", first(numbers))
print("smallest:", smallest(numbers))
print("first:", first(numbers))