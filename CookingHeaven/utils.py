import os
import sys


def is_test():
    return len(sys.argv) > 1 and sys.argv[1] == 'test'
