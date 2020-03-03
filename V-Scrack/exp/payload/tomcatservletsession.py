#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if apache tomcat servlet session operate vul')
    status = ''
    contentlen = ''
    dirconurl = url+'/nodirinthiswebanx4dm1n/'
    try:
        dirresponse=requests.get(dirconurl, verify=False, timeout=10)
        status=dirresponse.status_code
        contentLen=dirresponse.headers['content-length']
        servletpath = '/examples/servlets/servlet/SessionExample'
        servleturl=url+servletpath.strip('\r\n')
        response=requests.get(servleturl, verify=False, timeout=10)
        if response.headers['content-length']!=contentLen and 'SessionExample' in response.text and 'Session Attribute' in response.text :
            msg = 'Found /examples/servlets/servlet/SessionExample dir in url:'+servleturl+''
            print(msg)
            number = 'v38'
            return True,url,number,msg
        else:
            msg = 'Cannot found /examples/servlets/servlet/SessionExample dir in url:'+servleturl+'.'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

