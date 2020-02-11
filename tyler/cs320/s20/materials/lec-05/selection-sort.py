def selection_sort(L):
    for i in range(len(L)):
        idx_min = i
        for j in range(i, len(L)):
            if L[j] < L[i]:
                idx_min = j
        L[idx_min], L[i] = L[i], L[idx_min]

nums = [2, 4, 3, 1]
selection_sort(nums)
print(nums)
