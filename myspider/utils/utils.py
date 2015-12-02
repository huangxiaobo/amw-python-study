# -*- encoding=utf8 -*-
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"


def disable():
	HEADER = ''
	OKBLUE = ''
	OKGREEN = ''
	WARNING = ''
	FAIL = ''
	ENDC = ''


def infog( msg):
	print OKGREEN + msg + ENDC

def info( msg):
	print OKBLUE + msg + ENDC

def warn( msg):
	print WARNING + msg + ENDC

def err( msg):
	print FAIL + msg + ENDC

__report_indent = [0]
def debug(fn):
	"""Decorator to print information about a function call for use while debugging.
	Prints function name, arguments, and call number when the function is called. Prints this information
	again along with the return value when the function returns.
	"""

	def wrap(*params,**kwargs):
		call = wrap.callcount = wrap.callcount + 1

		indent = ' ' * __report_indent[0]
		fc = "%s(%s)" % (fn.__name__, ', '.join(
			[a.__repr__() for a in params[1:]] +
			["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
		))

		print "%s%s called [#%s]" % (indent, fc, call)
		__report_indent[0] += 1
		ret = fn(*params,**kwargs)
		__report_indent[0] -= 1
		print "%s%s returned %s [#%s]" % (indent, fc, repr(ret), call)

		return ret
	wrap.callcount = 0
	return wrap