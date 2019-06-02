# coding=utf-8

from application.bioinfo.process1 import process1_1
import sys


def main():
    try:
        process1_1()
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(11)


if __name__ == '__main__':
    main()