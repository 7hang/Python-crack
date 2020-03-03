#-*- coding: utf-8 -*-

import socket

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if zookeeper unanth vul')
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = b"envi"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if b'Environment' in data:
            msg = 'There is zookeeper unanth vul on url: ' + url + ' .'
            print(msg)
            number = 'v90'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        print(str(e))
    msg = 'There is no zookeeper unanth vul.'
    number = 'v0'
    return False, url, number, msg
