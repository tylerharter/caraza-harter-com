# can we find needle in the numbers list, or a sublist?
def search(numbers, needle):
    for x in numbers:
        if x == needle:
            return True
        elif type(x) == list:
            if search(x, needle):
                return True
    return False

values = [[1,2], [3,4], [5,6]]
print(search(values, 4))
