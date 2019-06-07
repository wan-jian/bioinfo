# coding=utf-8

from application import app
from application.bioinfo.process1 import process1_1
import sys


def main():
    try:
        app.do_processes()
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(11)


if __name__ == '__main__':
    main()