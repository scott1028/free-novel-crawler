#!/usr/bin/python3
# coding: utf-8

try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

h = HTMLParser()

import os
import re

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f[-4:].lower() == '.txt' and f[:5] != 'done-':
        with open(f, 'rb') as fd:
            buf = fd.read().decode('utf-8', 'ignore')#.encode('utf-8', 'ignore')
            tmp = h.unescape(buf)
            with open('done-' + f, 'w') as fd2:
                fd2.write(tmp)
