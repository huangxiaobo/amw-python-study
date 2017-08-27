# /usr/bin/env python
# -*- encoding=utf-8 -*-

class carried(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def __call__(self, *args, **kwargs):
        args = self.args + args
        if len(args) < self.func.func_code.co_argcount:
            return carried(self.func, *args)
        else:
            return self.func(*args)


@carried
def add(x, y):
    return x + y


add1 = add(1)

print add1(2)
