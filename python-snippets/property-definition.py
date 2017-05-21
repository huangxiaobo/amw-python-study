import sys

def propget(func):
	locals = sys._getframe(1).f_locals
	name = func.__name__
	prop = locals.get(name)
	print locals, type(locals), dir(locals)
	if not isinstance(prop, property):
		prop = property(func, doc=func.__doc__)
	else:
		doc = prop.__doc__ or func.__doc__
		prop = property(func, prop.fset, prop.fdel, doc)
	return prop


def propset(func):
	locals = sys._getframe(1).f_locals
	name = func.__name__
	prop = locals.get(name)
	print locals, type(locals), dir(locals)
	if not isinstance(prop, property):
		prop = property(func, doc=func.__doc__)
	else:
		doc = prop.__doc__ or func.__doc__
		prop = property(prop.fget, func, prop.fdel, doc)
	return prop

def propdel(func):
	locals = sys._getframe(1).f_locals
	name = func.__name__
	prop = locals.get(name)
	print locals, type(locals), dir(locals)
	if not isinstance(prop, property):
		prop = property(func, doc=func.__doc__)
	else:
		doc = prop.__doc__ or func.__doc__
		prop = property(prop.fget, prop.fset, func, doc)
	return prop

class ExampleOne(object):
	def __init__(self):
		self._half = 1

	@propget
	def myattr(self):
		return self._half * 2

	@propset
	def myattr(self, value):
		self._half = value / 2

	@propdel
	def myattr(self):
		del self._half


example =ExampleOne()
print example.myattr


class ExampleTwo(object):
	def __init__(self):
		self._half = 1

	@apply
	def myattr():
		def fget(self):
			return self._half

		def fset(self, value):
			self._half = value / 2

		def fdel(self):
			del self._half
		return property(**locals())

example_two = ExampleTwo()
example_two.myattr

class ExampleThree(object):
	def __init__(self):
		self._half = 1

