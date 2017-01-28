#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'utf-8'

def page(url):
    LOG(url, 'Start!')
    buf = getContent(url, TXTENCODE)

    reg_title = re.compile(u'<h1>《(?P<title>.*?)》')
    title = reg_title.search(buf).group('title')

    reg_host = re.compile(u'(?P<host>(?:http|https)://.*)/')
    base_url = reg_host.search(url).group('host')

    next_url = None
    for a_tag in re.compile(u'<a.*?>.*?</a>', re.DOTALL).finditer(buf):
        LOG(a_tag)
        pattern = re.compile(u'<a href="(?P<url>.*?)">下壹頁</a>', re.DOTALL)
        matched = pattern.search(a_tag.group(0))
        if matched != None:
            LOG(matched)
            path = matched.group('url')
            LOG(path)
            next_url = '%s%s' % (base_url, path)
            LOG(url)

    pattern = re.compile(u'<div id="BookContent">(?P<content>.*?)<div id="webPage" class="paginator">', re.DOTALL)
    matched = pattern.search(buf)
    if matched != None:
        buf = content_handle(matched.group('content'))
    else:
        buf = None
    LOG(url, 'Done!')
    return next_url, buf, title

def grab(url):
    idx = 1
    title = page(url)[2]
    with open('done-%s-%s.txt' % (re.sub(r'(?:\:|\\|\/)', '-', title), T), 'w') as fd:
        while url != None:
            url, buf, title = page(url)
            fd.write('\r\n第%s回\r\n' % idx)
            fd.write(buf)
            idx += 1

#
# ex: https://www.sto.cc/book-166701-1.html
# ex: https://www.sto.cc/book-166701-105.html
#
if __name__ == "__main__":
    LOG('ex: https://www.sto.cc/book-166701-103.html')
    url = input('target url?')
    grab(url)
