def is_positive_or_negative(num):
    if num > 0:
        return 'POSITIVE'
    elif num < 0:
        return 'NEGATIVE'
    else:
        return 'ZERO'


number = input('Enter a number: ')
number = int(number)
num_type = is_positive_or_negative(number)
print(num_type)