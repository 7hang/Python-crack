# coding:utf-8
import socket

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if memcache unauth vul')
    try:
        socket.setdefaulttimeout(10)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(b"stats\r\n")
        result = s.recv(1024)
        if b"STAT version" in result:
            msg = 'There is memcache unauth vul on url: ' +url+' .'
            print(msg)
            number = 'v71'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no memcache unauth vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',11211)
    print(res)