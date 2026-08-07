import sys


def err_and_exit(err_msg, exitcode=1):
    print(err_msg, file=sys.stderr)
    exit(exitcode)