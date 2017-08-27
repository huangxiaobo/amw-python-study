# /usr/bin/env python
# -*- encoding=utf-8 -*-

import sys
import threading
import time
import traceback


# https://stackoverflow.com/questions/1643327/sys-excepthook-and-threading

def my_except_hook(except_type, value, traceback):
    if except_type == KeyboardInterrupt:
        print "Handle code goes there"
    else:
        print 'Other exception.'
        sys.__excepthook__(except_type, value, traceback)


sys.excepthook = my_except_hook


def setup_thread_excepthook():
    """
    Workaround for `sys.excepthook` thread bug from:
    http://bugs.python.org/issue1230540

    Call once from the main thread before creating any threads.
    """

    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):

        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            try:
                run_original(*args2, **kwargs2)
            except Exception:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


class EmptyThread(threading.Thread):
    def run(self):
        while True:
            time.sleep(5)
            assert False


def main():
    setup_thread_excepthook()

    empty_thread = EmptyThread()
    empty_thread.daemon = True
    empty_thread.start()
    # assert False

    while True:
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print "catch exception :%s" % traceback.format_exc()
