# -*- coding:utf-8 -*-

import socket


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if iis 6.0 remote code execute vul(cve-2017-7269)')
    timeout = 5
    socket.setdefaulttimeout(timeout)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(port)
        sock.connect((ip,port))
        pay = b"OPTIONS / HTTP/1.0\r\n\r\n"
        sock.send(pay)
        data = sock.recv(2048)
        print(data)
        sock.close()
        if b"PROPFIND" in data and b"Microsoft-IIS/6.0" in data :
            msg = 'There is a iis 6.0 remote code execute vul on %s' %url
            number = 'v39'
            return True,url,number,msg
        else:
            msg = 'There is no iis 6.0 remote code execute vul on %s' %url
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','146.196.114.106',80)
    print(res)