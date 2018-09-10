#!/usr/bin/python
import subprocess, json, re, sys

PASS = 'PASS'
PROBLEMS = 20

def clean_lines(lines):
    return [l.strip() for l in lines if l.strip() != '']

# ignore whitespace and case
def are_lines_expected(actual_lines, expected_lines):
    actual_lines = clean_lines(actual_lines)
    expected_lines = clean_lines(expected_lines)
    if len(actual_lines) < len(expected_lines):
        return 'fewer output lines than expected'
    if len(actual_lines) > len(expected_lines):
        return 'more output lines than expected'
    for a,e in zip(actual_lines, expected_lines):
        if a.lower() != e.lower():
            return 'expected (%s) but found (%s)' % (e, a)
    return None

def problem1(lines):
    expected = [
        'one plus one is:',
        '2',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem2(lines):
    expected = [
        'two plus two is:',
        '4',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem3(lines):
    expected = [
        'the type of 5 is a(n):',
        "<class 'int'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem4(lines):
    expected = [
        'the type of 1.5 is a(n):',
        "<class 'float'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem5(lines):
    expected = [
        'the type of 5.0 is a(n):',
        "<class 'float'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem6(lines):
    expected = [
        'the type of "5.0" is a(n):',
        "<class 'str'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem7(lines):
    expected = [
        'the type of "True" is a(n):',
        "<class 'str'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem8(lines):
    expected = [
        'the type of False is a(n):',
        "<class 'bool'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem9(lines):
    expected = [
        'the type of 5>3 is a(n):',
        "<class 'bool'>",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem10(lines):
    expected = [
        'three plus four is:',
        "7",
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem11(lines):
    expected = [
        'here are 10 exclamation marks:',
        '!!!!!!!!!!',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem12(lines):
    expected = [
        'three times ten is:',
        '30',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem13(lines):
    try:
        answer = float(clean_lines(lines[-1]))
        if abs(answer-27) < 0.01:
            return PASS
    except:
        pass
    return 'expected 27'

def problem14(lines):
    try:
        answer = float(clean_lines(lines[-1]))
        if abs(answer-15424.418419015) < 0.01:
            return PASS
    except:
        pass
    return 'expected about $15,424'

def problem15(lines):
    expected = [
        "this is False: 321 is greater than 100 and less than 200",
        'True',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem15(lines):
    expected = [
        "this is False: 321 is greater than 100 and less than 200",
        'False',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem16(lines):
    expected = [
        'True',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem17(lines):
    expected = [
        'True',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem18(lines):
    expected = [
        'True',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem19(lines):
    expected = [
        'True',
    ]
    error = are_lines_expected(lines, expected)
    return error if error else PASS

def problem20(lines):
    try:
        answer = float(clean_lines(lines[-1]))
        if abs(answer-37.699111843077) < 0.25:
            return PASS
    except:
        pass
    return 'expected about $15,424'

def main():
    result = {'score': 0, 'tests': []}
    output = None
    program = 'main.py'
    if len(sys.argv) == 2:
        program = sys.argv[1]
    try:
        output = subprocess.check_output(['python3', program])
    except:
        print('Your Python program crashed.  Please fix it to get any points.')

    # did program even run successfully?
    if output:
        # normalize windows => unix, as a string (not bytes)
        output = str(output, 'utf-8')
        output = output.replace('\r\n', '\n')

        # chuck output lines by problem
        problem_number = None
        problems = dict() # key:problem number, val: list of lines
        for line in output.split('\n'):
            m = re.match(r'Problem (\d+)$', line)
            if m:
                problem_number = int(m.group(1))
                problems[problem_number] = []
            elif problem_number:
                problems[problem_number].append(line)

        # run checker on each section
        for problem_num in range(1, PROBLEMS+1):
            lines = problems.pop(problem_num, None)         # student code
            fn = globals().get('problem%d' % problem_num, None) # our test

            # did student produce output?
            if lines is None:
                result['tests'].append({
                    'test': problem_num,
                    'result': 'Problem %d output missing' % problem_num
                })
                continue

            # did we write the test yet?
            if not fn:
                result['tests'].append({
                    'test': problem_num,
                    'result': 'Test %d not written yet' % problem_num
                })
                continue

            # run test and record output
            test_result = fn(lines)
            result['tests'].append({
                'test': problem_num,
                'result': test_result
            })
        # final score
        passing = [t for t in result['tests'] if t['result'] == PASS]
        result['score'] = len(passing) * 100 // len(result['tests'])

    # save/display results
    with open('result.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
    print('RESULTS:')
    for test in result['tests']:
        print('  Problem %d: %s' % (test['test'], test['result']))
    print('Score: %d' % result['score'])

if __name__ == '__main__':
    main()

