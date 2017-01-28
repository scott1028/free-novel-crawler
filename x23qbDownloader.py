#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class X23QBNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div class="d_title">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<ul.*?id="chapterList".*?>.*?(?P<article>.*?)</ul', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li><a.*?href.*?="(?P<url>.*?)">.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'https://www.x23qb.com'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div id="TextContent".*?>(?P<content>.*?)<script>(?:chap_bg|style_bm)', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    X23QBNovelGrabber(TXTENCODE='gbk', tip='ex: https://www.x23qb.com/book/788/').run()
