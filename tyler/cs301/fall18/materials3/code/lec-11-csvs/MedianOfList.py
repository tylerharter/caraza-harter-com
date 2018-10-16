def find_median(l):
    l.sort()
    num_elems = len(l)
    if num_elems % 2 == 0:  # check if num_elems is even
        mid1 = l[(num_elems // 2) - 1]
        mid2 = l[num_elems // 2]
        mid_elem = (mid1 + mid2) / 2
        return mid_elem
    else:
        mid_elem = l[num_elems//2]
        return mid_elem



nums = [3, 1, 7, 4, 2, 6]
median = find_median(nums)
print('median =', median)
