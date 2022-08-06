#!/usr/bin/env python3
# coding: utf-8

from blessings import Terminal
from bs4 import BeautifulSoup

import abc
import re
from html.parser import HTMLParser
from urllib import request as urllib2
import urllib, socket
import http.cookiejar
from functools import reduce
import os
import re
import time
import multiprocessing.pool
import random
import json
import click


t = Terminal()

def content_handle(buf, treat_as_pure_text=os.environ.get('TXTMODE', '5').upper(), chapterType='text'):
    def _content_handle(buf, escape=False):
        LOG('MODE: %s' % treat_as_pure_text)
        buf = re.sub('<script.*?</script>', '', buf, flags=re.DOTALL)
        buf = re.sub('<style.*?</style>', '', buf, flags=re.DOTALL)
        buf = re.sub('<template.*?</template>', '', buf, flags=re.DOTALL)
        buf = re.sub('<fon.*?>.*?</font>', '', buf, flags=re.DOTALL)
        buf = re.sub('<!--.*?-->', '', buf, flags=re.DOTALL)
        if treat_as_pure_text == '1':
            buf = re.sub(r'<(.{0,1000}?)(?: |.){0,1000}?>(.{0,1000}?)</\1>', r'', buf, flags=re.DOTALL | re.DEBUG | re.VERBOSE)
        elif treat_as_pure_text == '2':
            buf = re.sub(r'<(.{0,1000}?)(?: |.){0,1000}?>(.{0,1000}?)</\1>', r'\2', buf, flags=re.DOTALL | re.DEBUG | re.VERBOSE)
        elif treat_as_pure_text == '3':
            buf = re.sub(r'<(.{0,1000}?)(?: |.){0,1000}?>(.{0,1000}?)</\1>', r'', buf, flags=re.DEBUG | re.VERBOSE)
        elif treat_as_pure_text == '4':
            buf = re.sub(r'<(.{0,1000}?)(?: |.){0,1000}?>(.{0,1000}?)</\1>', r'\2', buf, flags=re.DEBUG | re.VERBOSE)
        elif treat_as_pure_text == '5':
            soup = BeautifulSoup(buf, 'html.parser')  # default
            buf = soup.getText()
        elif treat_as_pure_text == '6':
            soup = BeautifulSoup(buf, 'html5lib')
            buf = soup.getText()
        elif treat_as_pure_text == '7':
            soup = BeautifulSoup(buf, 'lxml')
            buf = soup.getText()
        buf = H.unescape(buf)
        buf = re.sub(r'(?:&[A-Za-z]*;)', '', buf)
        buf = re.sub(r'(?:\r)', '', buf)
        buf = re.sub(r'(?:\n　+)', '\n', buf)
        buf = re.sub(r'(?:\n +)', '\n', buf)
        buf = re.sub(r'(?:“)+', ' ', buf)
        buf = re.sub(r'(?:”)+', ' ', buf)
        buf = re.sub(r'(?:\n)+', '\r\n', buf)
        buf = re.sub(r'(?:\r\n )', '\r\n', buf)
        buf = re.sub(r'(?:\0)', '', buf)
        buf = re.sub(r'(?:\x3f)+', '', buf)
        buf = re.sub(r'(?:\xa0)+', '', buf)
        buf = re.sub(r'(?:)', '', buf)
        buf = re.sub(r'(?:\.)+\.', '…', buf)
        buf = re.sub(r'(?:‥|…)+', '…', buf)
        buf = re.sub(r'(?:♦)+', '...', buf)
        buf = re.sub(r'(?:\.\.\.\r\n\.\.\.\r\n)+', '...\r\n', buf)
        buf = re.sub(r'(?:<br.*?/>)+', '\r\n', buf)
        buf = re.sub(r'(?:\n)+', '\n', buf)
        buf = re.sub(r'(?:\r)+', '\r', buf)
        buf = re.sub(r'(?:\r\n)+', '\r\n', buf)
        buf = re.sub(r'^(?:\t)+', '', buf, flags=re.MULTILINE)
        buf = re.sub(r'^(?:\xa0| )*', r'', buf, flags=re.MULTILINE)
        buf = re.sub(r'^(?:\xa0| |\u3000)*', r'', buf, flags=re.MULTILINE)
        buf = re.sub(r'h3>(?P<title>.*?)/h3>', '\\g<title>', buf, flags=re.MULTILINE)  # for biquge
        for i in set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒ ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠ 々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻ ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…~*♦'''):
            if i in set(u'():?[].!*'):
                buf = buf.replace(i + i, i)
                buf = buf.replace(i + i + ' ', i)
            else:
                buf = re.sub(r'(?:' + i + '+)', i, buf)
                buf = re.sub(r'(?:' + i + ' +)', i, buf)
        buf = re.sub(r'(?:\r)', '', buf)
        buf = re.sub(r'(?:\.)+\n(?:\.)+', '...', buf, flags=re.DOTALL)
        buf = re.sub('< */ *(.*?)>', '', buf, flags=re.DOTALL)
        return buf, escape
    escape = True
    prev = ''
    buf, escape = _content_handle(buf, True)
    curr = buf
    while prev != curr:
        LOG('prev: %s' % len(prev))
        prev = buf
        buf, escape = _content_handle(buf, escape)
        curr = buf
        LOG('curr: %s' % len(curr))
    # Invoked only once#1
    buf = re.sub(r'(?:\n\.\n)', '\n...\n', buf)
    buf = re.sub(r'(?:\.)+(.)', r'.\1', buf)
    buf = re.sub(r'(?:‥|…)+\n(?:‥|…)+', '…', buf, flags=re.DOTALL)
    buf = re.sub(r'(?:\t)+', '', buf, flags=re.MULTILINE)
    buf = re.sub(r'(?: )+$', '', buf, flags=re.MULTILINE)

    # NOTE: remove duplicated symbol
    buf = re.sub(r'((?:﹖|﹗|。|？|！))(?=\1)', '', buf, flags=re.DOTALL)

    # NOTE: add wrap after those symbol
    # buf = re.sub(r'((?:﹖|﹗|。|？|！))', '\g<0>\r\n', buf, flags=re.DOTALL)

    # NOTE: remove duplicated wrap
    buf = re.sub(r'((?:\r*\n))+', '\g<1>', buf, flags=re.DOTALL)

    # Filter special unicode
    def _filter_unicode(char):
        _char = char.group(0)
        # Ref: https://zh.wikipedia.org/wiki/Unicode#.E6.BC.A2.E5.AD.97.E5.95.8F.E9.A1.8C
        # Ref: https://gist.github.com/shingchi/64c04e0dd2cbbfbc1350
        # Ref: http://www.programmer-club.com.tw/ShowSameTitleN/general/4309.html
        CONDITION = [
            int('3001', 16) <= ord(_char) <= int('303F', 16),  # CJK 標點符號; Note: 0x3000 is a empty space
            int('0020', 16) <= ord(_char) <= int('007E', 16),  # 0-9a-zA-Z & 半形符號
            int('4E00', 16) <= ord(_char) <= int('FFEF', 16),  # Unicode CJK 常用字
        ]
        if reduce(lambda prev, curr: prev or curr, CONDITION):
            return _char
        else:
            return ''

    def _content_modifier(buf, chapterType):
        def handler(char):
            try:
                chapterNo = char.group('chapterNo')
                chapterName = char.group('chapterName')
            except Exception as e:
                return char.group(0)
            return f'第{chapterNo}章 {chapterName}'
        if chapterType == 'number':
            buf = re.sub(r'(?P<chapterNum>\d+)\r?\n', r'\n\n第\g<chapterNum>章\n\n', buf, flags=re.MULTILINE)
        else:
            pattern = r'^(?P<chapterNo>\d+) (?P<chapterName>.*)\n'
            buf = re.sub(pattern, handler, buf, flags=re.MULTILINE)
        return buf
    buf = re.sub(r'(?:.)', _filter_unicode, buf, flags=re.MULTILINE)
    sto_pattern = r'每一天新文都需要大家的支持才能成長起來，求推薦，求留言，感謝大家的支持|本作品由思兔網提供下載與在線閱讀|思兔網文檔下載與在線閱讀|思兔文檔共享與在線閱讀|思兔在線閱讀|本作品由思兔在線閱讀網友整理上傳|思兔網|\(猫扑中文 www\.mpzw\.com\)|猫扑中文|www\.mpzw\.com|'
    buf = re.sub(re.compile(sto_pattern, re.DOTALL), '', buf)
    buf = _content_modifier(buf, chapterType)
    buf = '\r\n%s\r\n' % buf
    # NOTE: add final wrap and avoid duplicated wrap at the end of content
    return re.sub(r'((?:\r*\n))+$', '\r\n', buf, flags=re.MULTILINE)

def parallel_handle(returnable_func=lambda x: x, input_array=[], worker_num=6, timeout=3):
    # Ref: https://jingsam.github.io/2015/12/31/multiprocessing.html
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(worker_num)
    results = []
    for i in range(0, len(input_array)):
        result = pool.apply_async(returnable_func, args=(input_array[i], ))
        results.append(result)
    pool.close()
    pool.join()
    return [result.get(timeout=timeout) for result in results]

    # Old Version, cause futex deadLock sometime
    # pool = multiprocessing.pool.ThreadPool(worker_num)
    # resp = pool.map(returnable_func, input_array)
    # pool.close()
    # pool.join()
    # resp = iter(resp)
    # return resp

def getContent(url, TXTENCODE=None, max_tries=10):
    counter = 0
    buf = ''
    while counter <= max_tries:
        try:
            LOG(url, '[Start]', '(tried count: %s)' % counter)
            version = str(int(random.random() * 10 + 70))
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.1916.47 Safari/537.36' % version
                }
            )
            fd = OPENER.open(req, timeout=7)
            if TXTENCODE == None:
                buf = fd.read()
            else:
                buf = H.unescape(fd.read().decode(TXTENCODE, 'ignore'))
            LOG(url, '[Done]', '(tried count: %s)' % counter)
            break
        except Exception as e:
            LOG(e, url, counter)
            counter += 1
            time.sleep(counter)
    if buf == '':
        ERROR(url)
    return buf

def LOG(*msg):
    try:
        print(', '.join([str(obj) for obj in msg]))
    except Exception as e:
        print(e)

def ERROR(*msg):
    try:
        print(', '.join([str(obj) for obj in msg]))
        _msg = reduce(lambda x, y: '%s %s' % (str(x), str(y)), msg)
        with open('error.txt', 'a') as fd:
            fd.write('%s %s\r\n' % (T, _msg))
    except Exception as e:
        print(e)

def getProxyFile():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files.sort()
    pattern = '(?P<timestamp>\d+).proxy'
    targets = list(filter(re.compile(pattern).match, files)) # Read Note
    targets.sort(reverse=True)
    if len(targets) >= 1:
        proxyFile = targets[0]
        lastTimestamp = int(re.compile(pattern).match(proxyFile).group('timestamp'))
    else:
        proxyFile = None
        lastTimestamp = 0
    return {
        'path': proxyFile,
        'timestamp': lastTimestamp,
    }

def generateProxyList():
    # Ref: https://free-proxy-list.net/anonymous-proxy.html

    def test_if_proxy_nowork(obj):
        socket.setdefaulttimeout(6)

        def is_bad_proxy(obj):    
            try:
                proxy_obj = {
                    'http': 'http://%(host)s:%(port)s' % obj, 
                }
                if obj.get('https') == 'yes':
                    proxy_obj['https'] = 'https://%(host)s:%(port)s' % obj       
                # print(proxy_obj)
                proxy_handler = urllib.request.ProxyHandler(proxy_obj)
                opener = urllib.request.build_opener(proxy_handler)
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                resp = opener.open('http://hole-puncher.herokuapp.com/')
                # print(resp.read())
            except urllib2.HTTPError as e:        
                print('Error code: ', e.code)
                return True
            except Exception as detail:
                print("ERROR:", detail)
                return True
            return False

        return is_bad_proxy(obj)

    fileInfo = getProxyFile()
    delta = ((time.time() - fileInfo.get('timestamp')) > 60 * 10)

    if not delta:
        return fileInfo
    LOG('expired by', delta, fileInfo)

    url = 'https://free-proxy-list.net/anonymous-proxy.html'
    buf = getContent(url, 'utf-8')

    pattern = ('<tr.*?' +
               '<td.*?>(?P<host>.*?)</td>.*?' +
               '<td.*?>(?P<port>.*?)</td>.*?' +
               '<td.*?>(?P<code>.*?)</td>.*?' +
               '<td.*?>(?P<country>.*?)</td>.*?' +
               '<td.*?>(?P<type>.*?)</td>.*?' +
               '<td.*?>(?P<google>.*?)</td>.*?' +
               '<td.*?>(?P<https>.*?)</td>.*?' +
               '<td.*?>(?P<lastCheck>.*?)</td>' +
               '')

    reg_url = re.compile(pattern, re.DOTALL)
    proxyList = []

    for i in reg_url.finditer(buf):
        obj = {
            'host': i.group('host'), 
            'port': i.group('port'), 
            'code': i.group('code'), 
            'country': i.group('country'), 
            'type': i.group('type'), 
            'google': i.group('google'), 
            'https': i.group('https'), 
            'lastCheck': i.group('lastCheck'), 
        }
        if re.match('^[0-9\.]+$', obj.get('host')) != None:
            # if obj.get('lastCheck').find('second') == -1:
            if len(proxyList) >= 10:
                continue
            obj['test_pass'] = not test_if_proxy_nowork(obj)
            if obj.get('test_pass') == True:
                proxyList.append(obj)
                print(obj)

    data = json.dumps(proxyList, indent=4)
    newTimestamp = int(time.time())
    newFileName = '%s.proxy' % newTimestamp
    with open(newFileName, 'w') as fd:
        fd.write(data)
    return {
        'path': newFileName,
        'timestamp': newTimestamp,
    }

CJ = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CJ))
T = str(int(time.time()))
H = HTMLParser()

flag = os.environ.get('PROXY', 'false').upper()
if flag == 'TRUE':
    fileInfo = generateProxyList()
    with open(fileInfo.get('path'), 'r') as fd:
        store = json.loads(fd.read())
        idx = int(random.random() * len(store))
        obj = store[idx]
        proxy_obj = {
            'http': 'http://%(host)s:%(port)s' % obj, 
        }
        if obj.get('https') == 'yes':
            proxy_obj['https'] = 'https://%(host)s:%(port)s' % obj       
        proxy_handler = urllib.request.ProxyHandler(proxy_obj)
        OPENER = urllib.request.build_opener(proxy_handler)
        LOG('Installed Proxy', proxy_obj)
        LOG('Proxy Detail',  obj)
