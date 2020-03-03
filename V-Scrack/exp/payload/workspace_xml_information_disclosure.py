#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if workspace project setting information disclose vul')
    newurl = url + '/.idea/workspace.xml'
    try:
        response = requests.get(newurl,verify=False,timeout=5)
        if '<component name' in response.text and '<project version="4">' in response.text:
            msg = 'Found workspace project setting information disclose vul in url:' + newurl + ' .'
            print(msg)
            number = 'v93'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no workspace project setting information disclose vul'
    number = 'v0'
    return False, url, number, msg