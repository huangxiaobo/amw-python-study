# /usr/bin/env python
# -*- encoding=utf-8 -*-

import json
import warlock

my_schema = {
    'properties': {
        'name': {'type': 'string'},
        'id': {'type': 'integer'},
    },
    'additionalProperties': False,
    'required': ['name', 'id']
}

if __name__ == '__main__':

    ErrorInfo = warlock.model_factory(my_schema)
    s = '[{"name":"aa", "id":1}, {"name":"bb", "id":2}]'

    lst = json.loads(s)
    if not isinstance(lst, list):
        exit()

    try:
        for item in lst:
            ErrorInfo(item)
            print item
    except Exception as e:
        print e.message
