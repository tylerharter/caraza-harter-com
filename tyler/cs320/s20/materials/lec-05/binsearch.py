# assume L is already sorted
def binary_search(L, target):
    left_idx = 0 # inclusive
    right_idx = len(L) # exclusive

    # keep splitting our list in half, until
    # it's length is <= 1
    while right_idx - left_idx > 1:
        mid_idx = (right_idx + left_idx) // 2
        mid = L[mid_idx]

        # throw away left or right half?
        if target >= mid:
            left_idx = mid_idx
        else:
            right_idx = mid_idx

    # did we cut down to a list of length 1 containing target?
    return right_idx > left_idx and L[left_idx] == target

L = [1, 2, 9, 42, 60, 70, 80, 99]
found = binary_search(L, 80)
print(found)
