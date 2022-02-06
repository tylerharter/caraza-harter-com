def hi():
    print("hi")

def call_n_times(f, n):
    for i in range(n):
        f()

call_n_times(f=hi, n=3)
