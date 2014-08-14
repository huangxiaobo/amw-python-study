#!/usr/bin/python
#!-*-encoding=utf-8 -*-

import abc

class Base(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractproperty
	def value(self):
		return 'Should nerver get here'

class Implementation(Base):
	@property
	def value(self):
		return 'concrete property'

try:
	b = Base()
	print 'Base.value:', b.value
except Exception, err:
	print 'ERROR', str(err)

i = Implementation()
print 'Implementation.value: ', i.value