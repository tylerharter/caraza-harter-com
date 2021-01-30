from subprocess import check_output

def beep(n=1):
    """makes n beeps"""
    check_output(["say", "-v", "Victoria"] + ["beep"] * n)
