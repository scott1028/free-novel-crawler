#!/usr/bin/env python3
# coding: utf-8

import os
os.environ['PROXY'] = 'True'

from lib import *


TXTENCODE = 'gbk'

if __name__ == "__main__":
    LOG('ex: http://www.webqxs.com/0/99/')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<h1.*?class="story-title">(?P<title>.*?)</h1>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    reg_article = re.compile(u'<div class="ml_list">(?P<article>.*?)<div class="footer">', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<a.*?(?:(href|onclick))=.*?"(?P<url>(?!(http|99999)).*?.html)".*?>', re.DOTALL)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    url_pool = ['%s%s' % (url, i.group('url')) for i in reg_url.finditer(buf) if i.group('url') != '.html']
    url_pool = url_pool[retrive_start:]
    buf_pool = parallel_handle(getContent, url_pool, 10)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_content = re.compile(u'<.*?class="read-content".*?>(?P<content>.*?)</p>', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n第%s回\r\n' % idx)
                fd.write(buf)
                idx += 1
