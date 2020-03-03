#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if htaccess file disclose vul')
    newurl = url + '/.htaccess'
    try:
        response = requests.get(newurl,verify=False,timeout=5)
        if 'RewriteEngine on' in response.text:
            msg = 'Found htaccess file disclose vul in url:' + newurl + ' .'
            print(msg)
            number = 'v94'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no htaccess file disclose vul'
    number = 'v0'
    return False, url, number, msg