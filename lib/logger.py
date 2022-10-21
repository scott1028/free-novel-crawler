#!/usr/bin/env python3
# coding: utf-8

from functools import reduce

def LOG(*msg):
    try:
        print(', '.join([str(obj) for obj in msg]))
    except Exception as e:
        print(e)

def ERROR(*msg):
    try:
        print(', '.join([str(obj) for obj in msg]))
        _msg = reduce(lambda x, y: '%s %s' % (str(x), str(y)), msg)
        with open('error.txt', 'a') as fd:
            fd.write('%s %s\r\n' % (T, _msg))
    except Exception as e:
        print(e)
