#!/usr/bin/python

import linecache
from linecache_data import *

filename = make_tempfile()

# The cache always returns a string, and uses
# an empty string to indicate a line wtich does
# not exist.
not_there = linecache.getline(filename, 500)
print '\nNOT THERE : "%s" includes %d characters' % (not_there, len(not_there))

cleanup(filename)

