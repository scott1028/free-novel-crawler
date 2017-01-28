#!/usr/bin/env python3
# coding: utf-8

from lib import *


TXTENCODE = 'utf-8'

def novel_url(novel_id, txt_id):
    return 'https://static.qinxiaoshuo.com/book/bookdata/%(novel_id)s/%(txt_id)s.txt' % { 'novel_id': novel_id, 'txt_id': txt_id }

if __name__ == "__main__":
    LOG('ex: https://www.qinxiaoshuo.com/book/%E5%BC%80%E6%8C%82%E8%8D%AF%E5%B8%88%E7%9A%84%E5%BC%82%E4%B8%96%E7%95%8C%E6%97%85%28%E5%BC%80%E6%8C%82%E8%8D%AF%E5%B8%88%E7%9A%84%E5%BC%82%E4%B8%96%E7%95%8C%E4%B9%8B%E6%97%85%29')
    url = input('target url?')
    retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
    if len(retrive_start) != 0:
        retrive_start = int(retrive_start)
    else:
        retrive_start = 0
    buf = getContent(url, TXTENCODE)
    reg_title = re.compile(r'.*?<meta property="og:novel:book_name" content="(?P<title>.*?)"', re.DOTALL)
    title = reg_title.search(buf).group('title')
    reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
    base_url = reg_host.search(url).group('host')
    reg_url = re.compile(u'<div.*?class=".*?chapter.*?">.*?href="(?P<url>.*?)".*?</div>', re.MULTILINE)
    html_url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf)]
    html_url_pool = html_url_pool[retrive_start:]
    txt_id_pool = [re.match(r'.*?(?P<txt_id>\d+)$', url).group('txt_id') for url in html_url_pool]
    novel_id = re.search(r'https://static.qinxiaoshuo.com/book/bookimg/(?P<novel_id>\d+).jpg', buf).group('novel_id')
    url_pool = [novel_url(novel_id, txt_id) for txt_id in txt_id_pool]
    buf_pool = parallel_handle(getContent, url_pool, 3)
    idx = 1
    with open('done-%s-%s.txt' % (title, T), 'w') as fd:
        for buf in buf_pool:
            buf = buf.decode(TXTENCODE, 'ignore')
            buf = content_handle(buf, '5')
            fd.write('\r\n第%s回\r\n' % idx)
            fd.write(buf)
            idx += 1
