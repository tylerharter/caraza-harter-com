def abs(x):
    if x < 0:
        return -x
    elif x > 0:
        return x

tests = []
def test(fn):
    tests.append(fn)
    return fn

@test
def test_neg():
    assert abs(-1) == 1
    assert abs(-3) == 3

@test
def test_pos():
    assert abs(1) == 1
    assert abs(3) == 3

@test
def test_zero():
    assert abs(0) == 0

passing = 0
failing = 0
for test_fn in tests:
    try:
        test_fn()
        passing += 1
    except Exception:
        failing += 1
print("PASS", passing, "FAIL", failing)
