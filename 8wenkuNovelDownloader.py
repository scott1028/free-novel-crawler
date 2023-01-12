#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class EightWenkuNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div.*?id="title">(?P<title>.*?)</div>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(
            '<table.*?class="css".*?>.*?(?P<article>.*?)</table>', re.DOTALL
        )
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(
            '<td class="ccss">.*?<a.*?href.*?="(?P<url>.*?)".*?>.*?</td>', re.MULTILINE
        )
        return reg_url

    def get_base_novel_link_url_prefix(self, url=None):
        return re.match(r"(?P<url>https{0,1}://.*/).*", url).groupdict().get("url")

    def get_novel_content_reg(self):
        reg_content = re.compile(
            '<div id="content".*?>(?P<content>.*?)</div>', re.DOTALL
        )
        return reg_content


if __name__ == "__main__":
    EightWenkuNovelGrabber(
        TXTENCODE="gbk", tip="ex: https://www.wenku8.net/novel/2/2586/index.htm"
    ).run()
