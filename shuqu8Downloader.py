#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'gbk'

if __name__ == "__main__":
    LOG('ex: http://www.shuqu8.com/0_312/')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'<div class="btitle">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
    title = reg_title.search(buf).group('title')
    reg_article = re.compile(u'<dl class="chapterlist">(?P<article>.*?)<div class="notice"', re.DOTALL)
    buf = reg_article.search(buf).group('article')
    reg_url = re.compile(u'<dd><a href="(?P<url>.*?)">.*?</a>', re.MULTILINE)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*)/')
    base_url = reg_host.search(url).group('host')
    url_pool = ['%s/%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf)]
    url_pool = url_pool[retrive_start:]
    # url_pool = ['http://www.shuqu8.com/0_312/163196.html']
    buf_pool = parallel_handle(getContent, url_pool, 100)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            reg_chapter = re.compile(u'<div.*?id="BookCon".*?<h1>(?P<chapter>.*?)</h1>', re.DOTALL)
            reg_chapter_matched = reg_chapter.search(buf)
            chapter = ''
            if reg_chapter_matched != None:
                chapter = reg_chapter_matched.group('chapter')
            chapter = chapter.replace(u'章节目录 ', '')
            reg_content = re.compile(u'<div id="BookText">(?P<content>.*?)<div class="ad_content_bottom">', re.DOTALL)
            reg_content_matched = reg_content.search(buf)
            if reg_content_matched != None:
                buf = content_handle(reg_content_matched.group('content'))
                fd.write('\r\n\r\n第%s回 %s\r\n\r\n' % (idx, chapter))
                fd.write(buf)
                idx += 1
