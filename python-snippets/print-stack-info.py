# /usr/bin/env python
# -*- encoding=utf-8 -*-

import sys
import traceback


def print_stack_info():
    if sys.platform == 'win32':
        try:
            import inspect
            for frame in inspect.stack():
                print '%s: %d, %s' % (frame[1], frame[2], frame[3])
        except:
            print 'can\'t print_stack_info'

    try:
        1 / 0
    except:
        print 'error:', traceback.format_exc()


if __name__ == "__main__":
    print_stack_info()
