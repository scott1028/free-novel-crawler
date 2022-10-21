#!/usr/bin/env python3
# coding: utf-8
# Kept but no used for now

import urllib
import socket
from urllib import request as urllib2
import os
import re
import time
import random
import json

from logger import LOG
from . import getContent

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
                proxy_handler = urllib.request.ProxyHandler(proxy_obj)
                opener = urllib.request.build_opener(proxy_handler)
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
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
