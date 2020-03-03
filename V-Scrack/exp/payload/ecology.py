# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if ecology vul')
    http = httpparse()
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/main.jsp')
        if tm[0] ==302 and re.search(b'login/Login.jsp',tm[2],re.I):
            msg = 'e-cology vul'
            number = 'v20'
            print(msg)
            return True,url,number,msg
        elif http.httpreq('GET', protocol, ip, port, '/weaver/weaver.email.FileDownloadLocation2')[0] == 500:
            if http.httpreq('GET', protocol, ip, port, '/weaver/weaver.email.FileDownloadLocation')[0] == 200:
                msg = 'may have e-cology sql vul'
                number = 'v20'
                print(msg)
                return True,url,number,msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no e-cology'
    number = 'v0'
    return False,url,number,msg
