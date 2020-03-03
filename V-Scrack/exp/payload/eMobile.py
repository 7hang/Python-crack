# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    http = httpparse()
    print('testing if e-Mobile backstage')
    try:
        #header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        tm = http.httpreq('GET', protocol, ip, port, '/login.do')
        if tm[0] == 200 and re.search(b'e-Mobile',tm[2],re.I):
            msg = 'e-Mobile backstage is:'+url+'/login.do'
            number = 'v21'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'Ther is no e-Mobile backstage'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
