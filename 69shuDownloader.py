#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'gbk'

if __name__ == "__main__":
    LOG('ex: http://www.69shu.com/13945/')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<div.*?class="mu_h1">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    title = title.replace('最新章节列表', '')
    reg_article = re.compile(u'<h2><span class="mu_ico"></span>正文</h2>(?P<article>.*?)<div.*?class="hot_tuijian".*?>', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<li.*?>.*?<a href="(?P<url>.*?)">.*?</li>', re.DOTALL)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    base_url = reg_host.search(url).group('host')
    url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf) if i.group('url').find(u' ') == -1]
    url_pool = url_pool[retrive_start:]
    buf_pool = parallel_handle(getContent, url_pool, 50)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_content = re.compile(u'<script>txttopshow3\(\);</script>(?P<content>.*?)<script>tool2\(\);</script>', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n第%s回\r\n' % idx)
                fd.write(buf)
                idx += 1
