option = int(input('Enter (1) for km to miles or (2) for miles to km: '))

if option == 1:
    km = float(input('Enter distance in km: '))
    miles = km * 0.6213
    print(km, 'km =', miles, 'miles')
elif option == 2:
    miles = float(input('Enter distance in miles: '))
    km = miles * 1.609
    print(miles, 'miles =', km, 'km')
else:
    print('Option is invalid')
