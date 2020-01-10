x = -6
if x > 0:
    if x % 2 == 0:
        print('positive and even')
    else:
        print('positive and odd')
elif x < 0:
    x = -x
    if x % 2 == 0:
        print('negative and even')
    else:
        print('negative and odd')
else:
    print('error!')
    print('please do not use 0')