#!/usr/bin/python
#!-*- coding:utf-8 -*-

import codecs
import sys

text = u'pi: π'

# Printing to stdout may cause an encoding error
print 'Default encoding:', sys.stdout.encoding
print 'TTY:', sys.stdout.isatty()
print text
