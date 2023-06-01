#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class Novel543NovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(
            r"<div.*?class=\"headline\">.*?<h1.*?>(?P<title>.*?)</h1>", re.DOTALL
        )
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(
            '<div.*?class="read".*?>.*?<dl>.*?</dl>.*?<dl>(?P<article>.*?)</dl>',
            re.DOTALL,
        )
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile('<a.*?href="(?P<url>.*?)".*?>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url=None):
        return "https://www.novel543.com"

    def get_novel_content_reg(self):
        reg_content = re.compile(
            '<div.*?class="content".*?>.*?<p>(?P<content>.*)<div.*?class="warp my-3 foot-nav"',
            re.DOTALL,
        )
        return reg_content

    def get_novel_content_next_page_url_req(self):
        reg_next_page_url = re.compile(
            '<span.*?class="next item-navbar-text">.*?<a.*?href="(?P<url>.*?)".*?>',
            re.DOTALL,
        )
        return None


if __name__ == "__main__":
    Novel543NovelGrabber(
        TXTENCODE="utf-8", tip="ex: https://www.novel543.com/0401320355/dir"
    ).run()
