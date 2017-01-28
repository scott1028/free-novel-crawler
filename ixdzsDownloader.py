#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber


class IxdzsNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'<div.*?class="d_info".*?>.*?<h1>(?P<title>.*?)</h1>', re.DOTALL)
        return reg_title

    def get_article_area_reg(self):
        reg_article = re.compile(r'<div.*?id="i-chapter".*?>.*?(?P<article>.*?)</div>', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(r'<li.*?><a.*?href.*?="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'https://tw.ixdzs.com'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(r'<div.*?class.*?=.*?"content".*?>(?P<content>.*?)<div.*?class="line".*?>', re.DOTALL)
        return reg_content

if __name__ == "__main__":
    IxdzsNovelGrabber(TXTENCODE='utf-8', tip='ex: https://tw.ixdzs.com/novel/%E9%83%BD%E5%B8%82%E4%BB%99%E7%8E%8B').run()
