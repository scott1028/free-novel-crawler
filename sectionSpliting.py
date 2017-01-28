#!/usr/bin/env python3
# coding: utf-8

from lib import *


if __name__ == "__main__":
    txtencode = input('encoding?')
    h = HTMLParser()
    t = str(int(time.time()))

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files.sort()
    chunks = []
    buf = []
    for f in files:
        matched = re.match('^done-(?P<title>.*?)(?P<ext>(?:.txt$|php$))', f)
        if matched == None:
            continue
        avaliable_matched = matched
        idx = 0
        with open(f, 'rb') as fd:
            buf = fd.read().decode(txtencode, 'ignore')
            for i in re.finditer('(?:(\n\d+\..*?\n)|(\n\d+ \w+.*?\n))', buf):
                idx += 1
                buf = buf.replace(i.group(0), '\r\n第%s回\r\n' % idx + i.group(0))
            with open('splited-%s-%s%s' % (avaliable_matched.group('title'), T, avaliable_matched.group('ext')), 'w') as fd2:
                fd2.write(buf)
