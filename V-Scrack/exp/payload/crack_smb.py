#  -*- coding:utf-8 -*-

from smb.SMBConnection import SMBConnection
import socket
from exp.lib.gla import getpassdict
import random


def ip2hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        pass
    try:
        query_data = "\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20\x43\x4b\x41\x41" + \
                     "\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41" + \
                     "\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x00\x00\x21\x00\x01"
        dport = 137
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.sendto(query_data, (ip, dport))
        x = _s.recvfrom(1024)
        tmp = x[0][57:]
        hostname = tmp.split("\x00", 2)[0].strip()
        hostname = hostname.split()[0]
        return hostname
    except:
        pass

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if smb weak pass vul')
    socket.setdefaulttimeout(15)
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    #psw = random.sample(psw, 4)
    user_list = ['administrator']
    hostname = ip2hostname(ip)
    if not hostname:
        msg = 'Therer is no smb weakpass vul in url:' +url+'.'
        number = 'v0'
        return False,url,number,msg
    for user in user_list:
        for pass_ in psw:
            try:
                pass_ = str(pass_.replace('{user}', user))
                conn = SMBConnection(user,pass_,'vulscan',hostname)
                if conn.connect(ip) == True:
                    print(pass_)
                    if pass_ == 'anonymous':
                        msg = 'There is an anonymous sharing, please check whether there is a sensitive file.'
                        print(msg)
                        number = 'v64'
                        conn.close()
                        return True,url,number,msg
                    else:
                        msg = 'There is smb weak pass vul on: %s , with username: %s and password: %s.' %(url,user,pass_)
                        print(msg)
                        number = 'v64'
                        conn.close()
                        return True,url,number,msg
                else:
                    pass
            except Exception as e:
                pass

    conn.close()
    msg = 'Therer is no smb weakpass vul in url:' +url+'.'
    number = 'v0'
    return False,url,number,msg
