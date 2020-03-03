# -*- coding:utf-8 -*-

import socket

def pstatus(ip, port, banner):
    msg = ip + ':' + port + 'is not vulnerable to authentication bypass .'
    return msg

def ptimeout(ip, port, banner):
    msg = ip + ':' + port + 'has timed out. '
    return msg

def ppatch(ip, port, banner):
    msg = ip + ':' + port + 'has been patched .'
    return msg

def pvulnerable(ip, port, banner):
    msg = ip + ':' + port + 'is likely VULNERABLE to authentication bypass .'
    return msg

def bannergrab(ip, port):
    try:
        s = socket.socket()
        s.connect((ip,int(port)))
        s.settimeout(5)
        banner = s.recv(1024)
        s.close()
        return banner
    except Exception as e:
        pass
    return ""

def verify(protocol,ip,port):
    url = ip + ':' + str(port)
    print('testing if cve-2018-10933 libSSH-Authentication-Bypass vul')
    results = []
    try:
        results.append([ip,port,bannergrab(ip,port)])
        for result in results:
            if result[2]:
                if b"libssh-0.6" in result[2]:
                    msg = pvulnerable(result[0], result[1], result[2])
                    print(msg)
                    number = 'v91'
                    return True, url, number, msg
                elif b"libssh-0.7" in result[2]:
                    if int(result[2].split(".")[-1]) >= 6:
                        msg = ppatch(result[0], result[1], result[2])
                        print(msg)
                    else:
                        msg = pvulnerable(result[0], result[1], result[2])
                        print(msg)
                        number = 'v91'
                        return True, url, number, msg
                elif b"libssh-0.8" in result[2]:
                    if int(result[2].split(".")[-1]) >= 4:
                        msg = ppatch(result[0], result[1], result[2])
                        print(msg)
                    else:
                        msg = pvulnerable(result[0], result[1], result[2])
                        print(msg)
                        number = 'v91'
                        return True, url, number, msg
                else:
                    msg = pstatus(result[0], result[1], result[2])
                    print(msg)
            else:
                pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'Therer is no cve-2018-10933 libSSH-Authentication-Bypass vul on url:' + url + '.'
    number = 'v0'
    return False, url, number, msg












