class Fab(object):
	def __init__(self, max):
		self.max = max
		self.n, self.a, self.b = 0, 0, 1

	def __iter__(self):
		return self

	def next(self):
		if self.n < self.max:
			result = self.b
			self.a, self.b = self.b, self.a + self.b
			self.n += 1
			return result
		raise StopIteration()


def fab(max):
	n, a, b = 0, 0, 1
	while n < max:
		n += 1
		a, b = b, a + b
		yield b


for i in fab(10):
	print i

from inspect import isgeneratorfunction

print isgeneratorfunction(fab)
