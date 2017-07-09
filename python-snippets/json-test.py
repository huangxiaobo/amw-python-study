# -*- encoding=utf-8 -*-
import json

json_str = '{"name": "hxb", "age" : 1, "国籍" : "中国", "sub":[{"x":1}, {"y":2}]}'

json_obj = json.loads(json_str)

print json_obj, type(json_obj)

file = 'json-test.txt'

"""Serialize ``obj`` to a JSON formatted ``str``.

 If ``skipkeys`` is false then ``dict`` keys that are not basic types
 (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``)
 will be skipped instead of raising a ``TypeError``.

 If ``ensure_ascii`` is false, all non-ASCII characters are not escaped, and
 the return value may be a ``unicode`` instance. See ``dump`` for details.

 If ``check_circular`` is false, then the circular reference check
 for container types will be skipped and a circular reference will
 result in an ``OverflowError`` (or worse).

 If ``allow_nan`` is false, then it will be a ``ValueError`` to
 serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
 strict compliance of the JSON specification, instead of using the
 JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

 If ``indent`` is a non-negative integer, then JSON array elements and
 object members will be pretty-printed with that indent level. An indent
 level of 0 will only insert newlines. ``None`` is the most compact
 representation.  Since the default item separator is ``', '``,  the
 output might include trailing whitespace when ``indent`` is specified.
 You can use ``separators=(',', ': ')`` to avoid this.

 If ``separators`` is an ``(item_separator, dict_separator)`` tuple
 then it will be used instead of the default ``(', ', ': ')`` separators.
 ``(',', ':')`` is the most compact JSON representation.

 ``encoding`` is the character encoding for str instances, default is UTF-8.

 ``default(obj)`` is a function that should return a serializable version
 of obj or raise TypeError. The default simply raises TypeError.

 If *sort_keys* is ``True`` (default: ``False``), then the output of
 dictionaries will be sorted by key.

 To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
 ``.default()`` method to serialize additional types), specify it with
 the ``cls`` kwarg; otherwise ``JSONEncoder`` is used.

 """


def method_one():
	# saved as pretty json format
	with open(file, 'w') as fd:
		json.dump(json_obj, fd, indent=4, ensure_ascii=False, encoding='utf-8')


def method_two():
	# will not keep json format
	json_str = json.dumps(json_obj, indent=4, ensure_ascii=False, encoding='utf-8')
	with open(file, 'w') as fd:
		fd.write(json_str)


method_one()
# method_two()
