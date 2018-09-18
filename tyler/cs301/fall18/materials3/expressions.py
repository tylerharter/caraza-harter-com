#!/usr/bin/python
import random, time

def math_gen():
    operand_count = random.randint(1,3)
    nums = [-2, -1, 0, 1, 2, 4]
    parts = [random.choice(nums) for i in range(operand_count)]
    ops = [random.choice(['+', '-', '/', '*', '**']) for i in range(operand_count-1)]
    out = str(parts[0])
    for op, part in zip(ops, parts[1:]):
        out += ' '+op+' '+str(part)
    return out

def comparison_gen():
    op = random.choice(['<', '<=', '==', '>', '>=', '!='])
    return '%s %s %s' % (math_gen(), op, math_gen())

def logic_gen():
    operand_count = random.randint(2,3)
    parts = [comparison_gen() for i in range(operand_count)]
    ops = [random.choice(['and', 'or']) for i in range(operand_count-1)]
    out = parts[0]
    for op, part in zip(ops, parts[1:]):
        out += ' '+op+' '+part
    return out

def main():
    while True:
        expr = logic_gen()
        try:
            result = str(eval(expr))
        except:
            result = 'error'

        # test the user
        print('Consider this expression:\n')
        print(expr + '\n')
        
        answer = ''
        while not answer in ['t', 'f', 'e']:
            answer = input("Is it True[t], False[f], or an error[e]? ")
        answer = {'t':'True', 'f':'False', 'e':'error'}[answer]
        if answer == result:
            print('GOOD!')
            time.sleep(1)
        else:
            print('Oops, the actual result was: ' + result)
            time.sleep(3)
        print('\n\n')

if __name__ == '__main__':
    main()
