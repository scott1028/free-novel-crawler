#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'cp950'

if __name__ == "__main__":
    LOG('ex: http://www.ck101.org/120/120756/')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<script>mb_mulu1\(\);</script>.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    reg_article = re.compile(u'class="novel_list".*?>(?P<article>.*?)<script>mb_bottom\(\);</script>', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<dd>.*?<a href="(?P<url>.*?)".*?>.*?</dd>', re.DOTALL)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    base_url = reg_host.search(url).group('host')
    url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf) if i.group('url').find(u' ') == -1]
    url_pool = url_pool[retrive_start:]
    buf_pool = parallel_handle(getContent, url_pool, 50)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_content = re.compile(u'<*?id="content".*?>(?P<content>.*?)<script.*?id="jquery_\d+".*?>', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n第%s回\r\n' % idx)
                fd.write(buf)
                idx += 1
