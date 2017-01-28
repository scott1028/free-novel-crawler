#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class EightBookNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<h2.*?>(?P<title>.*?)</h2>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(u'<div.*?class="subtitles".*?>(?P<article>.*?)</div>', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li.*?>.*?<a.*?href="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        return 'https://8book.com'

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div.*?id="text".*?>(?P<content>.*?)<div.*?', re.DOTALL)
        return reg_content

    def get_novel_content_next_page_url_req(self):
        reg_next_page_url = re.compile(u'<span.*?class="next item-navbar-text">.*?<a.*?href="(?P<url>.*?)".*?>', re.DOTALL)
        return None

if __name__ == "__main__":
    EightBookNovelGrabber(TXTENCODE='utf-8', tip='ex: https://8book.com/novelbooks/138546/').run()
