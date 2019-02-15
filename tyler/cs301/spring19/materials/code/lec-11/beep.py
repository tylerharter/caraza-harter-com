from subprocess import check_output

def beep():
    check_output(["say"] + ["beep"] * 8)
