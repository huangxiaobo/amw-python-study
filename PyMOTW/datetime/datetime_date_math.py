#!/usr/bin/python
#!-*- coding:utf-8 -*-

import datetime

today=  datetime.date.today()
print 'Today    :', today

one_day = datetime.timedelta(days = 1)
print 'One day  :', one_day

yesterday = today - one_day
print 'Yesterday    :', yesterday

tomorrow = today + one_day
print 'Tomorrow     :', tomorrow

print 'tomorrow - yesterday:', tomorrow - yesterday
print 'yesterday - tomorrow:', yesterday - tomorrow
