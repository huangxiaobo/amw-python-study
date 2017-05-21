#-*- encoding=utf-8 -*-
import json

s = '{"name": "hxb", "age" : 1, "sub":[{"x":1}, {"y":2}]}'

d = json.loads(s)

print d, type(d)

file = 'json-test.txt'

with open(file, 'w') as f:
	json.dump(d, f, indent=4)