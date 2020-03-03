# -*- coding:utf-8 -*-


from exp.lib.gla import getpassdict
import socket

def verify(protocol,ip,port):
    host = ip+':'+str(port)
    timeout = 3
    print('testing if redis unauth vul')
    msg = 'There is no redis unauth vul'
    number = 'v0'
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append(' ')
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(b"INFO\r\n")
        result = s.recv(1024)
        if b"redis_version" in result:
            msg = 'There is a redis unauthorized access , password is None'
            print(msg)
            number = 'v11'
            return True,host,number,msg
        elif b"Authentication" in result:
            for ps in psw:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                s.send("AUTH %s\r\n" % (ps))
                result = s.recv(1024)
                if b'+OK' in result:
                    msg = 'There is a redis unauthorized access , password is %s' %ps
                    print(msg)
                    number = 'v11'
                    return True,host,number,msg
                else:
                    pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,host,number,msg
    return False,host,number,msg

if __name__ == '__main__':
    res = verify('http','43.255.226.195',6379)
    print(res)