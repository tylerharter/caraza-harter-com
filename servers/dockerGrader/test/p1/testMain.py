# UW-Madison CS301 Test Script
import argparse
# import boto3
from io import StringIO
import json
import os
# import resource
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS301 test monitor')
    parser.add_argument('-i', '--id', help='set student id', required=True)
    parser.add_argument('-p', '--project', help='set project name', required=True)
    args = parser.parse_args()

    try:
        os.remove("result.json")
    except OSError:
        pass

    errorLog = {}
    try:
        subprocess.check_output(
            ["python3", "test.py"],
            # don't generate pycache. It caused permission error when running
            # in docker environment.
            env={"PYTHONDONTWRITEBYTECODE": "1"},
            universal_newlines=True,
            stdin=open("io/default.txt", "r"), # default.txt is an empty file
            stderr=subprocess.STDOUT,
            timeout=3) # timeout: 3s
    except subprocess.CalledProcessError as err:
        errorLog = {"error": "Error: return non-zero status ({}). STDOUT: {}".format(
                    err.returncode, err.output)}
    except subprocess.TimeoutExpired as err:
        errorLog = {"error": "Error: Timeout"} # Use 504 here for timeout
    except Exception as e:
        errorLog = {"error": "Error: Other exception({})".format(str(e))}
    # check the existence of result.json
    if not errorLog and not os.path.exists("result.json"):
        errorLog = {'errorCode': "Error: result.json not found"}
    if errorLog:
        with open("result.json", "w") as fw:
            json.dump(errorLog, fw)
