# coding:utf-8
import socket

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if memcache drdos vul')
    try:
        socket.setdefaulttimeout(10)
        data = "set i 0 0 1048501" + "\r\n" + 'i' * 1048501 + "\r\n"
        data = data.encode(encoding="utf-8")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.send(data)
        result = s.recv(1024)

        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = "\x00\x00\x00\x00\x00\x01\x00\x00get VUKIC539IHDR62DS4\r\n"
        data = data.encode(encoding="utf-8")
        udpClient.sendto(data, (ip, int(port)))
        data, addr = udpClient.recvfrom(1024)

        if b'STORED' in result and b'END' in data:
            msg = 'There is memcache drdos vul on url: ' +url+' .'
            print(msg)
            number = 'v79'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no memcache drdos vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',11211)
    print(res)