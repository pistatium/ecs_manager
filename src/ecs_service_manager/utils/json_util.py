# coding: utf-8

import datetime
import json

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    return x

def json_dumps(data):
    return json.dumps(data, default=datetime_handler, indent=4)

