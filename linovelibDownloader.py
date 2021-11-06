#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class LinovelibNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div class="book-meta">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<div.*?class="volume-list".*?>.*?(?P<article>.*?)<div class="pages">', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li.*?>.*?<a.*?href.*?="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'https://www.linovelib.com'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div id="TextContent".*?>(?P<content>.*?)<p class="mlfy_page">', re.DOTALL)
        return reg_content

    def get_next_page_req(self):
        reg_next_section = re.compile(u'<p.*?class="mlfy_page">.*<a href="(?P<url>.*?)">下一页</a>', re.DOTALL)
        return reg_next_section

    def url_pool_filter(self):
        return re.compile(u'.*?javascript.*?', re.DOTALL)

if __name__ == "__main__":
    LinovelibNovelGrabber(TXTENCODE='utf-8', tip='ex: https://www.linovelib.com/novel/2796/catalog').run()
