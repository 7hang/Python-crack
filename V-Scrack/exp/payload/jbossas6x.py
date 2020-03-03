#-*- coding: utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if CVE-2017-12149 JBOSS AS 6.x unserialized vul')
    http = httpparse()
    tag = 'JBoss Web'
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/invoker/readonly')
        if (re.search(tag,str(tm[2]),re.I)) and tm[0] == 500:
            msg = 'There is CVE-2017-12149 JBOSS AS 6.x unserialized vul on url: ' +url+ ' .'
            number = 'v62'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2017-12149 JBOSS AS 6.x unserialized vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','223.202.25.77',80)
    print(res)