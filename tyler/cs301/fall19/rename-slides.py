import os, sys, re

dry = False

with open('schedule.txt') as f:
    schedule = f.read()

    
def get_num(path):
    parts = path.split('/')[1].replace('.', '-').split('-')
    if len(parts) >= 2 and re.match(r'\d\d', parts[1]):
        return int(parts[1])
    return None


def lec_nums(paths):
    nums = set()
    for path in paths:
        num = get_num(path)
        if num != None:
            nums.add(get_num(path))
    return sorted(nums)


def delete(paths, num):
    for path in paths:
        if get_num(path) == num:
            print('delete ' + path)
            assert(schedule.find(path) < 0)
            if not dry:
                os.remove(path)


def rename(paths, num1, num2):
    global schedule
    for path in paths:
        if get_num(path) == num1:
            pos = path.index('-')
            path2 = path[:pos+1] + '%02d'%num2 + path[pos+3:]
            print('%s => %s' % (path, path2))
            schedule = schedule.replace(path, path2)
            if not dry:
                os.rename(path, path2)


def main():
    paths = [os.path.join("materials", name) for name in os.listdir("materials")]
    nums = lec_nums(paths)

    if len(sys.argv) != 3:
        print('bad args')
        return

    cmd = sys.argv[1]
    num = int(sys.argv[2])
    if cmd == 'pop':
        delete(paths, num)
        for n in nums:
            if n > num:
                rename(paths, n, n-1)
    elif cmd == 'push':
        for n in reversed(nums):
            if n >= num:
                rename(paths, n, n+1)
    else:
        print("bad cmd")


    with open('schedule.tmp' if dry else 'schedule.txt', 'w') as f:
        f.write(schedule)


if __name__ == '__main__':
    main()
