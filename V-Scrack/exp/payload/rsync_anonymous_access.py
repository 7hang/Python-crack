# coding:utf-8

import socket
import logging


def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if rsync anonymous access vul')
    logging.basicConfig(level=logging.INFO,format="%(message)s")
    socket.setdefaulttimeout(5)
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((ip,int(port)))
        helloString = "405253594e43443a2033312e300a"
        client.send(bytes.fromhex(helloString))
        hellodata = client.recv(1024)
        if hellodata.find(b"@RSYNCD") >= 0:
            xmessage = "0a"
            client.send(bytes.fromhex(xmessage))
            while True:
                data = client.recv(1024)
                if data == "":
                    break
                else:
                    if str(data).find("@RSYNCD: EXIT") >= 0:
                        if data == b"@RSYNCD: EXIT\n":
                            msg = 'There is no rsync unauth anonymous access vul'
                            number = 'v0'
                            return False, url, number, msg
                        else:
                            msg = 'There is rsync unauth anonymous access vul on url: ' +url+' . '
                            print(msg)
                            number = 'v85'
                            return True,url,number,msg
                    else:
                        pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no rsync unauth anonymous access vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','47.110.172.226',873)
    print(res)

