from read_numbers import *

open_file('nums.txt')

counter = 0
while has_next():
    counter += get_next()
    print('partial sum: ' + str(counter))

print('final: ' + str(counter))

# has_next returns True, if and only if get_next()
# will return an actual number (not None) next time it's called