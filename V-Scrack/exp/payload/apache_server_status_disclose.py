#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if apache server status information disclose vul')
    newurl = url + '/server-status/'
    try:
        response = requests.get(newurl,verify=False,timeout=3)
        if 'PID' in response.text and 'Idle cleanup of worker' in response.text and 'Scoreboard Key' in response.text:
            msg = 'Found apache server status information disclose vul in url:' + newurl + ' .'
            print(msg)
            number = 'v98'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no apache server status information disclose vul'
    number = 'v0'
    return False, url, number, msg