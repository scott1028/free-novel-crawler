#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class EightWenkuNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div id="info">.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(
            '<div.*?id="list".*?>.*?(?P<article>.*?)</div', re.DOTALL
        )
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(
            '<dd>.*?<a.*?href.*?="(?P<url>.*?)".*?>.*?</dd>', re.MULTILINE
        )
        return reg_url

    def get_base_novel_link_url_prefix(self, url=None):
        novel_link_url_prefix = "http://www.8wenku.com"
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(
            '<div id="content".*?>(?P<content>.*?)</div>', re.DOTALL
        )
        return reg_content


if __name__ == "__main__":
    EightWenkuNovelGrabber(TXTENCODE="gbk", tip="ex: http://www.8wenku.com/b/385").run()
