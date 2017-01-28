#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'gbk'

if __name__ == "__main__":
    LOG('ex: http://www.mpzw.com/html/138/138375/index.html')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<div.*?class="Main">.*?<h1>(?P<title>.*?)<span>.*?</h1>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    reg_article = re.compile(u'<ul id="chapterlist">(?P<article>.*?)<div id="tuijian">', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<a.*?href="(?P<url>.*?)".*?>', re.DOTALL)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    base_url = reg_host.search(url).group('host')
    url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf)]
    url_pool = url_pool[retrive_start:]
    buf_pool = parallel_handle(getContent, url_pool, 50)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_content = re.compile(u'<div.*?class="Content".*?id="content".*?>(?P<content>.*?)<(?:div|DIV) align="center">', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n第%s回\r\n' % idx)
                fd.write(buf)
                idx += 1
