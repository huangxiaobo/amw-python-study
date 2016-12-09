def getStackInfo():
	if sys.platform == 'win32':
		import inspect
		stackInfo = ''
		for frame in inspect.stack():
			stackInfo += ('%s: %d, %s'%(frame[1], frame[2], frame[3]) + '\n')
			stackInfo += (frame[4][0] + '\n')
		return stackInfo
	else:
		return ''