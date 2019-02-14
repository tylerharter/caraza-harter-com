from subprocess import check_output

def beep(n=1):
    check_output(["say", "-v", "Victoria"] + ["beep"] * n)
