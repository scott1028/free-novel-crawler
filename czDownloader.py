#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class CzNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<span class="title">(?P<title>.*?)</span>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<ul.*?id="chapter-list".*?>.*?(?P<article>.*?)</ul>', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li><a.*?href.*?="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'https:'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div.*?class.*?=.*?"content".*?>(?P<content>.*?)<div.*?class.*?=.*?"notice">', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    CzNovelGrabber(TXTENCODE='utf-8', tip='ex: https://czbooks.net/n/uh8aj').run()
