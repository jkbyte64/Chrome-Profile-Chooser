import os
import sys


def resource_path(rpath):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, rpath)


def err_and_exit(err_msg, exitcode=1):
    print(err_msg, file=sys.stderr)
    exit(exitcode)