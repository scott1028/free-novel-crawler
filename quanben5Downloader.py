#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class Quanben5NovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div.*?class="topbar">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<div.*?class="wrapper".*?>(?P<article>.*?)<div class="footer".*?>', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li.*?class="c3">.*?<a href="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'http://big5.quanben5.com'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div.*?id="content".*?>(?P<content>.*?)<div.*?class="nlist_page"', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    Quanben5NovelGrabber(TXTENCODE='utf-8', tip='ex: http://big5.quanben5.com/n/quanseshengxiang/xiaoshuo.html').run()
