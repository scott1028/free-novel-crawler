#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class TsnwbNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div.*?id="info".*?>.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<div.*?id="list".*?>.*?<ul.*?class="chapters".*?>.*?(?P<article>.*?)</ul>', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li.*?class="chapter".*?><a.*?href.*?="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'http://www.tsnwb.org'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div.*?id="content".*?>(?P<content>.*?)<div.*?class.*?=.*?"bottem2">', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    TsnwbNovelGrabber(TXTENCODE='gbk', tip='ex: http://www.tsnwb.org/7_7964/').run()
