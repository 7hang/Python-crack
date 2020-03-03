#-*- coding: utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if CVE-2017-7504 JBOSSMQ JMS colony unserialized vul')
    http = httpparse()
    tag = 'This is the JBossMQ HTTP-IL'
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/jbossmq-httpil/HTTPServerILServlet')
        if (re.search(tag,str(tm[2]),re.I)) and tm[0] == 200 and (re.search('JBoss',str(tm[1]),re.I)):
            msg = 'There is CVE-2017-7504 JBOSSMQ JMS colony unserialized vul on url: ' +url+ ' .'
            number = 'v61'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2017-7504 JBOSSMQ JMS colony unserialized vul'
    number = 'v0'
    return False,url,number,msg