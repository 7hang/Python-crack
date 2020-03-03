# -*- coding:utf-8 -*-

import socket,time,re,base64
from exp.lib.gla import getpassdict

def _socket_connect(ip, port,msg = "test"):
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.sendall(bytes(msg, 'utf-8'))
        message = str(s.recv(1024))
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if smtp weak pass vul')
    user_list = ['admin', 'root', 'zte','10192989']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    if _socket_connect(ip,port):
        for username in user_list:
            for password in psw:
                try:
                    socket.setdefaulttimeout(5)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    banner = str(s.recv(1024))
                    emailaddress = '.'.join(ip.split('.')[1:])
                    if "220" in banner:
                        s.send(bytes('HELO mail.' + emailaddress + ' \r\n', 'utf-8'))
                        helo = str(s.recv(1024))
                        if "250" in helo:
                            s.send(bytes('auth login \r\n', 'utf-8'))
                            authanswer = str(s.recv(1024))
                            if "334" in authanswer:
                                s.send(base64.b64encode(bytes(username, encoding='utf-8')) + b'\r\n')
                                useranswer = str(s.recv(1024))
                                if "334" in useranswer:
                                    s.send(base64.b64encode(bytes(password, encoding='utf-8')) + b'\r\n')
                                    passanswer = str(s.recv(1024))
                                    if "235" in passanswer:
                                        msg = 'There is smtp weak pass vul on: %s , with username: %s and password: %s.' % (url, username, password)
                                        print(msg)
                                        number = 'v204'
                                        return True, url, number, msg

                    s.close()
                except Exception as e:
                    print(str(e))
                    pass
    else:
        msg = 'Therer is no smtp weakpass vul in url:' + url + '.'
        number = 'v0'
        return False, url, number, msg
    msg = 'Therer is no smtp weakpass vul in url:' + url + '.'
    number = 'v0'
    return False, url, number, msg








