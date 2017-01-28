#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'gbk'

def parseBookMenu(url):
    LOG(url, 'Start!')
    output = []
    buf = getContent(url, TXTENCODE)

    reg_book_title = re.compile(u'<div.*?class="mu_h1">.*?<h1>(?P<book_title>.*?)</h1></div>')
    book_title = reg_book_title.search(buf).group('book_title').replace(u'全文阅读', '')

    chapter_block = re.compile(u'<ul class="mulu_list">(?P<chapter_block>.*?)</ul>', re.DOTALL)
    buf = chapter_block.search(buf).group('chapter_block')

    reg_content = re.compile(u'<li.*?>(?P<a_tag>.*?)</li>', re.MULTILINE)
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*)/')
    reg_link_title = re.compile(u'<a.*?>(?P<link_title>.*?)</a>')
    reg_link = re.compile(u'.*?href="(?P<path>.*?)"')

    base_url = reg_host.search(url).group('host')

    for match in reg_content.finditer(buf):
        a_tag = match.group('a_tag')
        # print a_tag
        reg_link_title_matched = reg_link_title.search(a_tag)
        if reg_link_title_matched != None:
            chapter = reg_link_title_matched.group('link_title')
        else:
            chapter = ''
        reg_link_matched = reg_link.search(a_tag)
        if reg_link_matched != None:
            path = reg_link.search(a_tag).group('path')
            url = '%s/%s' % (base_url, path)
            # print chapter, url
            output.append({
                'chapter': chapter,
                'url': url})
            LOG('Done! %s' % chapter)
        else:
            continue
    LOG(url, 'Done!')
    return {
        'title': book_title,
        'buf': output
    }

def getArticle(buf):
    reg_content = re.compile(u'<div.*?class="contentbox">(?P<content>.*?)</div>', re.DOTALL)    
    content = content_handle(reg_content.search(buf).group('content'))
    return content

def getContentDelayFactory(sec=5):
    def _getContent(url):
        LOG('>> Delay %s sec for url: %s' % (sec, url))
        time.sleep(sec)
        return getContent(url)
    return _getContent

if __name__ == "__main__":
    LOG('ex: http://www.ybdu.com/xiaoshuo/19/19160/')
    target_url = input('target url?')
    TXTENCODE = input('encoding?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    tmp = parseBookMenu(target_url)
    title = tmp.get('title')
    t = str(int(time.time()))
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        url_pool = [obj.get('url') for obj in tmp.get('buf')[retrive_start:]]
        chapter_pool = [obj.get('chapter') for obj in tmp.get('buf')[retrive_start:]]
        resp = parallel_handle(getContentDelayFactory(5), url_pool, worker_num=1)
        for buf in resp:
            buf = buf.decode(TXTENCODE, 'ignore')
            obj = getArticle(buf)
            fd.write('\r\n第%s回\r\n' % idx)
            fd.write(chapter_pool[idx - 1])
            fd.write(obj)
            idx +=1
