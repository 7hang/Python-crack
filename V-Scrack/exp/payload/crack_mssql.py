# coding:utf-8

import socket
import random
import binascii
from exp.lib.gla import getpassdict

def str2hex(x):
    asdad = bytes(x, 'utf-8')
    return asdad.hex()

def auth(host, port, username, password, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        hh = str2hex(host)
        husername = str2hex(username)
        lusername = len(username)
        lpassword = len(password)
        ladd = len(host) + len(str(port)) + 1
        hladd = hex(ladd).replace('0x', '')
        hpwd = str2hex(password)
        pp = str2hex(str(port))
        address = hh + '3a' + pp
        hhost = str2hex(host)
        data = "0200020000000000123456789000000000000000000000000000000000000000000000000000ZZ5440000000000000000000000000000000000000000000000000000000000X3360000000000000000000000000000000000000000000000000000000000Y373933340000000000000000000000000000000000000000000000000000040301060a09010000000002000000000070796d7373716c000000000000000000000000000000000000000000000007123456789000000000000000000000000000000000000000000000000000ZZ3360000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y0402000044422d4c6962726172790a00000000000d1175735f656e676c69736800000000000000000000000000000201004c000000000000000000000a000000000000000000000000000069736f5f31000000000000000000000000000000000000000000000000000501353132000000030000000000000000"
        data1 = data.replace(data[16:16 + len(address)], address)
        data2 = data1.replace(data1[78:78 + len(husername)], husername)
        data3 = data2.replace(data2[140:140 + len(hpwd)], hpwd)
        if lusername >= 16:
            data4 = data3.replace('0X', str(hex(lusername)).replace('0x', ''))
        else:
            data4 = data3.replace('X', str(hex(lusername)).replace('0x', ''))
        if lpassword >= 16:
            data5 = data4.replace('0Y', str(hex(lpassword)).replace('0x', ''))
        else:
            data5 = data4.replace('Y', str(hex(lpassword)).replace('0x', ''))
        hladd = hex(ladd).replace('0x', '')
        data6 = data5.replace('ZZ', str(hladd))
        data7 = bytes.fromhex(data6)
        sock.send(data7)
        packet = sock.recv(1024)
        if b'master' in packet:
            sock.close()
            return True
    except Exception as e:
        sock.close()
        return False

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if mssql weak pass vul')
    timeout = 15
    user_list = ['sa']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('sa')
    #psw = random.sample(psw, 4)
    for user in user_list:
        for pass_ in psw:
            try:
                pass_ = str(pass_.replace('{user}', user))
                result = auth(ip, port, user, pass_, timeout)
                if result == True:
                    msg = 'There is mssql weak pass vul on: %s , with username: %s and password: %s.' %(url,user,pass_)
                    print(msg)
                    number = 'v69'
                    return True,url,number,msg
                else:
                    pass
            except Exception as e:
                pass
    msg = 'Therer is no mysql weakpass vul in url:' +url+'.'
    number = 'v0'
    return False,url,number,msg