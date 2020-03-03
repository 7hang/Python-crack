#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if tomcat server hello.jsp has xss vul')
    newurl = url + '/tomcat-docs/appdev/sample/web/hello.jsp?test=<h1>cccjmzymtsx</h1>'
    try:
        response = requests.get(newurl,verify=False,timeout=3)
        if '<h1>cccjmzymtsx</h1>' in response.text and response.status_code == 200:
            msg = 'Found tomcat server hello.jsp has xss vul in url:' + newurl + ' .'
            print(msg)
            number = 'v106'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no tomcat server hello.jsp has xss vul'
    number = 'v0'
    return False, url, number, msg


