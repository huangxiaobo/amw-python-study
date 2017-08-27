# /usr/bin/env python
# -*- encoding=utf-8 -*-

class Lock(object):
    def __init__(self):
        self.lock_fp = None

    def __enter__(self):
        print 'enter lock'
        self.lock_fp = True
        return True

    def __exit__(self, *args):
        if self.lock_fp is not None:
            print 'exit lock'
            self.lock_fp = None


if __name__ == '__main__':
    with Lock() as lock:
        print 'process...'
