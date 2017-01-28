#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'gbk'

if __name__ == "__main__":
    LOG('ex: http://www.miaoshuwu.com/0/684/')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<div class="info">.*?<h2>(?P<title>.*?)</h2>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    # reg_article = re.compile(u'<div class="listmain">.*?(?P<article>.*?)<script', re.DOTALL)
    reg_article = re.compile(u'<dt>.*?正文卷</dt>.*?(?P<article>.*?)<script', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<dd><a href.*?="(?P<url>.*?)">.*?</dd>', re.MULTILINE)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    base_url = reg_host.search(url).group('host')
    url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf)]
    url_pool = url_pool[retrive_start:]
    buf_pool = parallel_handle(getContent, url_pool, 20)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_content = re.compile(u'<div id="content".*?>(?P<content>.*?)<div class="page_chapter">', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n第%s回\r\n' % idx)
                fd.write(buf)
                idx += 1
