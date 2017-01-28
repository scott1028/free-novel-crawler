#!/usr/bin/env python
# coding: utf-8

import re
import requests


a = open('input.txt', 'r')
b = a.read()
c = re.findall('href="(.*?)".*?>(.*?)<', b)

out = []

for url, title in c:
    try:
        res = requests.get(url)
        if res.status_code / 200 >= 2:
            raise Exception('fail')
        print res.status_code, title, url#, _url
    except:
        print 'fail', title, url
        out.append({
            'title': title,
            'url': url
        })

for row in out:
    fd = open('out.txt', 'w')
    fd.write(row['title'] + '\t' + row['url'] + '\r\n')
fd.close()
