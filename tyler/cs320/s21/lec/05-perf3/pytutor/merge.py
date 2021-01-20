def merge(L1, L2):
  rv = []
  idx1 = 0
  idx2 = 0

  while True:
    done1 = idx1 == len(L1)
    done2 = idx2 == len(L2)

    if done1 and done2:
      return rv

    choose1 = False
    if done2:
      choose1 = True
    elif not done1 and L1[idx1] < L2[idx2]:
      choose1 = True

    if choose1:
      rv.append(L1[idx1])
      idx1 += 1
    else:
      rv.append(L2[idx2])
      idx2 += 1

  return rv

def merge_sort(L):
  if len(L) < 2:
    return L
  mid = len(L) // 2
  left = L[:mid]
  right = L[mid:]
  left = merge_sort(left)
  right = merge_sort(right)
  return merge(left, right)

result = merge_sort([4, 1, 2, 3])
print(result)
