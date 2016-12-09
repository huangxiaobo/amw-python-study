# -*- coding: utf-8 -*-

def printStackInfo():
	if sys.platform == 'win32':
		try:
			import inspect
			for frame in inspect.stack():
				print '%s: %d, %s'%(frame[1], frame[2], frame[3])
		except:
			print 'can\'t printStackInfo'