#!/usr/bin/env python3
# coding: utf-8

from lib import *

# NOTE: issubclass(AnyClass(), NovelGrabber) ==> True / False
# Ref: https://realpython.com/python-interface/#using-metaclasses
# Ref: https://realpython.com/python-interface/#using-abstract-method-declaration
class NovelGrabber(metaclass=abc.ABCMeta):
    @classmethod
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'get_title_reg') and
            callable(subclass.get_title_reg) and
            hasattr(subclass, 'get_article_area_reg') and
            callable(subclass.get_article_area_reg) and
            hasattr(subclass, 'get_chapter_urls_reg') and
            callable(subclass.get_chapter_urls_reg) and
            hasattr(subclass, 'get_base_novel_link_url_prefix') and
            callable(subclass.get_base_novel_link_url_prefix) and
            hasattr(subclass, 'get_novel_content_reg') and
            callable(subclass.get_novel_content_reg) and
            hasattr(subclass, 'run') and
            callable(subclass.run)
        )

    def __init__(self, TXTENCODE='utf-8', tip='ex: https://czbooks.net/n/uh8aj'):
        self.TXTENCODE = TXTENCODE
        self.tip = tip
        pass

    def run(self):
        def parse_content(buf):
            reg_content = self.get_novel_content_reg()
            reg_content_matched = reg_content.search(buf)
            return reg_content_matched
        
        def write_content(matched_content, idx, sub_idx = ''):
            if reg_content_matched != None:
                buf = content_handle(matched_content.group('content'))
                fd.write('\r\n第%s回' % idx)
                if sub_idx != '':
                    fd.write(' - %s' % sub_idx)
                fd.write('\r\n')
                fd.write(buf)
                return True
            return False

        LOG(self.tip)
        url = input('target url?')
        retrive_start = input('Get From [n:]? ( To skip when you type empty string, `-5 -> [-5:]` ) ')
        if len(retrive_start) != 0:
            retrive_start = int(retrive_start)
        else:
            retrive_start = 0
        buf = getContent(url, self.TXTENCODE)
        reg_title = self.get_title_reg()
        title = reg_title.search(buf).group('title')
        reg_article = self.get_article_area_reg()
        # import pdb; pdb.set_trace()
        buf = reg_article.search(buf).group('article')
        reg_url = self.get_chapter_urls_reg()
        base_url = self.get_base_novel_link_url_prefix(url)
        url_pool = ['%s%s' % (base_url, i.group('url')) for i in reg_url.finditer(buf)]
        if self.url_pool_filter() != None:
            url_pool = [i for i in url_pool if self.url_pool_filter().match(i) == None]
        # url_pool = url_pool[0:10]
        url_pool = url_pool[retrive_start:]
        buf_pool = parallel_handle(getContent, url_pool, 20)
        idx = 1
        with open('done-%s-%s.txt' % (title, T), 'w') as fd:
            for buf in buf_pool:
                sub_idx = 1
                buf = buf.decode(self.TXTENCODE, 'ignore')
                reg_content_matched = parse_content(buf)
                if write_content(reg_content_matched, idx):
                    # NOTE: try flip page
                    try:
                        req_next_page_url = self.get_next_page_req()
                        matched_next_page_url = req_next_page_url.search(buf)
                        next_page_url = None
                        if matched_next_page_url != None:
                            next_page_url = matched_next_page_url.group('url')
                            print('next_page_url:' + next_page_url)
                        while next_page_url != None:
                            sub_buf = [val for val in parallel_handle(getContent, [self.get_base_novel_link_url_prefix(url) + next_page_url], 1)][0]
                            sub_buf = sub_buf.decode(self.TXTENCODE, 'ignore')
                            sub_reg_content_matched = parse_content(sub_buf)
                            write_content(sub_reg_content_matched, idx, sub_idx)
                            next_page_url = self.get_next_page_req()
                            matched_next_page_url = req_next_page_url.search(sub_buf)
                            next_page_url = None
                            if matched_next_page_url != None:
                                next_page_url = matched_next_page_url.group('url')
                            sub_idx += 1
                    except Exception as e:
                        print(e)
                    idx += 1

    @abc.abstractmethod
    def get_title_reg(self):
        # reg_title = re.compile(r'<span.*?class.*?=.*?"title">(?P<title>.*?)</span>', re.DOTALL)
        # return reg_title
        raise Exception('Not implemented for filename')

    @abc.abstractmethod
    def get_article_area_reg(self):
        # reg_article = re.compile(u'<ul.*?class.*?=.*?"nav chapter-list">.*?(?P<article>.*?)</ul>', re.DOTALL)
        # return reg_article
        raise Exception('Not implemented for article HTML DOM')

    @abc.abstractmethod
    def get_chapter_urls_reg(self):
        # reg_url = re.compile(u'<li><a.*?href.*?="(?P<url>.*?)".*?>.*?</li>', re.MULTILINE)
        # return reg_url
        raise Exception('Not implemented for parsing chapter urls')

    @abc.abstractmethod
    def get_base_novel_link_url_prefix(self, url = None):
        # reg_host = re.compile(u'(?P<host>(?:http|https)://.*?)/')
        # base_url = reg_host.search(url).group('host')
        # ...or
        # novel_link_url_prefix = 'https:'
        # return novel_link_url_prefix
        if url != None:
            novel_link_url_prefix_regex = re.compile('^(?P<host>https{0,1}://.*?)/')
            return novel_link_url_prefix_regex.search(url).group('host')
        raise Exception('Not implemented for chapter url link prefix')

    @abc.abstractmethod
    def get_novel_content_reg(self):
        # reg_content = re.compile(u'<div.*?class.*?=.*?"content".*?>(?P<content>.*?)<div.*?class.*?=.*?"notice">', re.DOTALL)
        # return reg_content
        raise Exception('Not implemented for each content of chapter')

    # NOTE: [OPTIONAL] if this novel has next page in sampe chapter, return this URL
    def get_next_page_req(self):
        return None

    # NOTE: [OPTIONAL] if this novel has next page in sampe chapter, return this URL
    def url_pool_filter(self):
        return None
