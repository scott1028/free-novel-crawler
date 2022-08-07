#!/usr/bin/env python3
#!/usr/bin/env python3
# coding: utf-8

import re

from lib.NovelGrabber import NovelGrabber

# WIP: not finished yet
class X23shuNovelGrabber(NovelGrabber):
    def get_title_reg(self):
        reg_title = re.compile(r'title=" (?P<title>.*?)"', re.DOTALL)
        return reg_title
        # return f'{int(time.time())}'

    def get_article_area_reg(self):
        reg_article = re.compile(u'(?P<article>.*)', re.DOTALL)
        return reg_article

    def get_chapter_urls_reg(self):
        reg_url = re.compile(u'<li><a.*?href.*?="(?P<url>.*?)">.*?</li>', re.MULTILINE)
        return reg_url

    def get_base_novel_link_url_prefix(self, url = None):
        novel_link_url_prefix = 'http://www.23shu.com'
        return novel_link_url_prefix

    def get_novel_content_reg(self):
        reg_content = re.compile(u'<div.*?id="chaptercontent".*?>(?P<content>.*?)<div.*? class="info bottominfo"', re.DOTALL)
        return reg_content

    def getFormatUrl(self, url):
        novelId = re.compile(u'.*/(?P<novelId>\d+)/?').search(url).group('novelId')
        return f'http://www.23shu.com/novelsearch/novel/getdlist/?id={novelId}&order=asc'

if __name__ == "__main__":
    # http://www.23shu.com/novelsearch/novel/getdlist/?id=6074&order=asc
    X23shuNovelGrabber(TXTENCODE='utf-8', tip='ex: http://www.23shu.com/novel/6074/').run()
