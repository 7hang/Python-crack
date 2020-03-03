# -*- coding:utf-8 -*-

import ssl
import socket
import sys

try:
    SSL_VERSION={
        #'SSLv3':ssl.PROTOCOL_SSLv3,
        #'SSLv2':ssl.PROTOCOL_SSLv2,
        'SSLv23':ssl.PROTOCOL_SSLv23,
        'TLSv1':ssl.PROTOCOL_TLSv1,
    }
except Exception as e:
    SSL_VERSION={
        #'SSLv3':ssl.PROTOCOL_SSLv3,
        'SSLv23':ssl.PROTOCOL_SSLv23,
        'TLSv1':ssl.PROTOCOL_TLSv1,
    }

def check_ssl_version(version,ip,port):
    try:
        https = ssl.SSLSocket(socket.socket(),ssl_version=SSL_VERSION.get(version))
        c = https.connect((ip,port))
        print(version + ' Supported')
        return True
    except Exception as e:
        return False

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    timeout = 5
    print('testing if poodle vul')
    try:
        port = int(port)
        socket.setdefaulttimeout(timeout)
        s = socket.socket().connect((ip,port))
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    try:
        ssl3 = check_ssl_version('SSLv3',ip,port)
        ssl2 = check_ssl_version('SSLv2',ip,port)
        ssl23 = check_ssl_version('SSLv23',ip,port)
        tls = check_ssl_version('TLSv1',ip,port)
        print(ssl3)
        if ssl3:
            msg = 'There is poodle vul on url: ' +url+ ' .'
            number = 'v16'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'There is no poodle vul on ' +url+ ' .'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','218.60.28.46',443)
    print(res)