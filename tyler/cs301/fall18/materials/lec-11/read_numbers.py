__nums = []
__pos = 0

def open_file(path):
    '''open_file(path) sets things up so you can get numbers from that file with get_next()'''
    global __nums, __pos
    with open(path) as f:
        __nums = [int(l.strip()) for l in f if l.strip()]
        __pos = 0

def get_next():
    '''get_next() returns the next integer from the opened file, or None if there are no numbers left'''
    global __nums, __pos
    if __pos >= len(__nums):
        return None
    val = __nums[__pos]
    __pos += 1
    return val

def has_next():
    '''has_next() checks whether we have more numbers in the file'''
    return not (__pos >= len(__nums))
