#!/usr/bin/python
# -*-encoding=utf-8 -*-
def simple_decorator(decorator):
	def new_decorator(f):
		g = decorator(f)
		g.__name__ = f.__name__
		g.__doc__ = f.__doc__
		g.__dict__.update(f.__dict__)
		return g

	new_decorator.__name__ = decorator.__name__
	new_decorator.__doc__ = decorator.__doc__
	new_decorator.__dict__.update(decorator.__dict__)
	return new_decorator


@simple_decorator
def my_simple_logging_decorator(func):
	def you_will_never_see_this_name(*args, **kwargs):
		print 'calling {}'.format(func.__name__)
		return func(*args, **kwargs)

	return you_will_never_see_this_name


@my_simple_logging_decorator
def double(x):
	""" Double the number """
	return x * 2


assert double.__name__ == 'double'
assert double.__doc__ == ' Double the number '
print double(10)


class Foo(object):
	def __init__(self):
		self.x = 42


foo = Foo()


def addto(instance):
	def decorator(func, *args, **kwargs):
		import types
		f = types.MethodType(func, instance, instance.__class__)
		setattr(instance, f.__name__, f)
		return f

	return decorator


@addto(foo)
def print_x(self):
	print self.x


foo.print_x()


####################################Counting function calls####################################
class countcalls(object):
	__instances = {}

	def __init__(self, f):
		self.__f = f
		self.__numcalls = 0
		countcalls.__instances[f] = self

	def __call__(self, *args, **kwargs):
		self.__numcalls += 1
		return self.__f(*args, **kwargs)

	@staticmethod
	def count(f):
		return countcalls.__instances[f].__numcalls

	@staticmethod
	def counts():
		return dict([(f, countcalls.__instances[f].__numcalls) for f in countcalls.__instances])


@countcalls
def f():
	print 'count calls.'


f()
f()
f()
print countcalls.counts()


####################################Alternate Counting function calls####################################
class countcalls(object):
	__instances = {}

	def __init__(self, f):
		self.__f = f
		self.__numcalls = 0
		countcalls.__instances[f] = self

	def __call__(self, *args, **kwargs):
		self.__numcalls += 1
		return self.__f(*args, **kwargs)

	def count(self):
		return countcalls.__instances[self.__f].__numcalls

	@staticmethod
	def counts():
		return dict([(f, countcalls.__instances[f].__numcalls) for f in countcalls.__instances])


@countcalls
def f():
	print 'count calls.'


f()
f()
f()

print f.count()
print f.counts()

####################################Generating Deprecation Warnings####################################
import warnings


def deprecated(func):
	def new_func(*args, **kwargs):
		warnings.warn("Call to deprecated function {0}.".format(func.__name__))
		return func(*args, **kwargs)

	new_func.__name__ = func.__name__
	new_func.__doc__ = func.__doc__
	new_func.__dict__.update(func.__dict__)
	return new_func


@deprecated
def some_old_function(x, y):
	return x + y


some_old_function(1, 2)
