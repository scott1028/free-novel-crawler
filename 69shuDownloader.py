#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class SixNineshuNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(
            r'<div.*?class="bread".*?>.*?<a.*</a>.*?<a.*?>(?P<title>.*?)</a>.*?</div>',
            re.DOTALL,
        )
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(
            '<div.*?id="catalog".*?>(?P<article>.*?)</div>',
            re.DOTALL,
        )
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(
            '<li.*?>.*?<a.*?href.*?="(?P<url>.*?)".*?>.*?</li>',
            re.MULTILINE,
        )
        return reg_url

    def get_base_novel_link_url_prefix(self, url=None):
        novel_link_url_prefix = ""
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(
            '<div.*?class="txtnav".*?>(?P<content>.*)</div>.*?<div.*?class.*?=.*?"page1">',
            re.DOTALL,
        )
        return reg_content


if __name__ == "__main__":
    SixNineshuNovelGrabber(
        TXTENCODE="gbk", tip="ex: https://www.69shu.com/A44201/"
    ).run()
