#!/usr/bin/python

import os

for i in range(10):
    print i, os.ttyname(i)
