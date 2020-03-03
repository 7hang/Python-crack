# -*- coding:utf-8 -*-

import requests
import base64

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if activemq weak pass vul')
    url += '/admin/'
    key = base64.b64encode(b"admin:admin").decode()
    headers = {'Authorization': 'Basic %s}' % key, 'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/45.0'}
    try:
        c = requests.get(url, headers=headers, timeout=5).content
        if b'Console' in c:
            msg = 'There is activemq weak pass vul on url: ' +url+ ' with userid and weakpass:admin+admin '
            print(msg)
            number = 'v33'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no activemq weak pass vul'
    number = 'v0'
    return False,url,number,msg