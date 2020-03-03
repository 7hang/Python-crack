__author__ = '10192989'
# coding: utf-8

import random
import socket
import hashlib
from exp.lib.gla import getpassdict

def make_response(username, password, salt):
    pu = hashlib.md5((password + username).encode(encoding='utf-8')).hexdigest()
    buf = hashlib.md5((pu.encode(encoding='utf-8')+salt)).hexdigest()
    return 'md5' + buf

def auth(host, port, username, password, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        packet_length = len(username) + 7 + len(
            "\x03user  database postgres application_name psql client_encoding UTF8  ")
        p = "%c%c%c%c%c\x03%c%cuser%c%s%cdatabase%cpostgres%capplication_name%cpsql%cclient_encoding%cUTF8%c%c" % (
        0, 0, 0, packet_length, 0, 0, 0, 0, username, 0, 0, 0, 0, 0, 0, 0, 0)
        p = p.encode(encoding='utf-8')
        sock.send(p)
        packet = sock.recv(1024)
        packet = packet.hex()
        if int(packet[:2]) == 52 or packet[0] == b'R':
            #authentication_type = str([packet[9]])
            #print(authentication_type)
            #c = int(authentication_type[4:6], 16)
            c = int(packet[17])
            if c == 5:
                salt = packet[-8:]
        else:
            return 3
        salt = bytes.fromhex(salt)
        lmd5 = make_response(username, password, salt)
        packet_length1 = len(lmd5) + 5 + len('p')
        pp = 'p%c%c%c%c%s%c' % (0, 0, 0, packet_length1 - 1, lmd5, 0)
        pp = pp.encode(encoding='utf-8')
        sock.send(pp)
        packet1 = sock.recv(1024)
        packet1 = packet1.hex()
        if int(packet1[:2]) == 52:
            return True
    except Exception as e:
        if "Errno 10061" in str(e) or "timed out" in str(e): return 3

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if postgresql weak pass vul')
    user_list = ['postgres','admin']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('postgres')
    psw.append('123456')
    #psw = random.sample(psw, 4)
    timeout = 5
    for user in user_list:
        for pass_ in psw:
            try:
                pass_ = str(pass_.replace('{user}', user))
                result = auth(ip, int(port), user, pass_, timeout)
                if result == 3:
                    break
                if result == True:
                    msg = 'There is postgresql weak pass vul on: %s , with username: %s and password: %s.' % (
                    url, user, pass_)
                    print(msg)
                    number = 'v115'
                    return True, url, number, msg
            except Exception as e:
                print(str(e))
                pass
    msg = 'Therer is no postgresql weakpass vul in url:' + url + '.'
    number = 'v0'
    return False, url, number, msg



