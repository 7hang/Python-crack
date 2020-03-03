#-*-coding:utf-8-*-

import requests
requests.adapters.DEFAULT_RETRIES = 5

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if phpinfo file disclose vul')
    newurl = url + '/phpinfo.php'
    try:
        response = requests.get(newurl,timeout=5,verify=False)
        if '<title>phpinfo()</title>' in response.text:
            msg = 'Found phpinfo file disclose vul in url:' + newurl + ' .'
            print(msg)
            number = 'v95'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no phpinfo file disclose vul'
    number = 'v0'
    return False, url, number, msg