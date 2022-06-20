#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class BiqugeNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div id="info">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<div.*?id="list".*?>.*?(?P<article>.*?)</div', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<dd>.*?<a.*?href.*?="(?P<url>.*?)".*?>.*?</dd>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        return url

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div id="content".*?>(?P<content>.*?)</div>', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    default_encode = 'gbk'
    encode = input(f'encode? (default: {default_encode})') or default_encode
    print('encode:', encode)
    BiqugeNovelGrabber(TXTENCODE=encode, tip='ex: https://www.xbiquge.so/book/33615/').run()
