#-*-coding:utf-8-*-

import socket
import struct

buf=b""
buf+=b"\x03\x00"
buf+=b"\x00\x0b"
buf+=b"\x06"
buf+=b"\xe0"
buf+=b"\x00\x00"
buf+=b"\x00\x00"
buf+=b"\x00"

connectinitialbuf=b""
connectinitialbuf+=b"\x03\x00\x00\x65"
connectinitialbuf+=b"\x02\xf0\x80"
connectinitialbuf+=b"\x7f\x65\x5b"
connectinitialbuf+=b"\x04\x01\x01"
connectinitialbuf+=b"\x04\x01\x01"
connectinitialbuf+=b"\x01\x01\xff"
connectinitialbuf+=b"\x30\x19"
connectinitialbuf+=b"\x02\x01\x22"
connectinitialbuf+=b"\x02\x01\x20"
connectinitialbuf+=b"\x02\x01\x00"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x00"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x02\xff\xff"
connectinitialbuf+=b"\x02\x01\x02"
connectinitialbuf+=b"\x30\x18"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x00"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\xff"
connectinitialbuf+=b"\x02\x01\x02"
connectinitialbuf+=b"\x30\x19"
connectinitialbuf+=b"\x02\x01\xff"
connectinitialbuf+=b"\x02\x01\xff"
connectinitialbuf+=b"\x02\x01\xff"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x01\x00"
connectinitialbuf+=b"\x02\x01\x01"
connectinitialbuf+=b"\x02\x02\xff\xff"
connectinitialbuf+=b"\x02\x01\x02"
connectinitialbuf+=b"\x04\x00"

userrequestbuf=b""
userrequestbuf+=b"\x03\x00"
userrequestbuf+=b"\x00\x08"
userrequestbuf+=b"\x02\xf0\x80"
userrequestbuf+=b"\x28"

channelrequestbuf=b""
channelrequestbuf+=b"\x03\x00\x00\x0c"
channelrequestbuf+=b"\x02\xf0\x80\x38"

def verify(protocol,ip,port):
    host = ip+':'+str(port)
    print('testing if ms12-020 vul')
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (ip,int(port))
    try:
        sock.connect(server_address)
        sock.sendall(buf)
        data = sock.recv(11)
        if b"\x03\x00\x00\x0b\x06\xd0\x00\x00\x12\x34\x00" in data:
            sock.sendall(connectinitialbuf)
            sock.sendall(userrequestbuf)
            userrequestdata = sock.recv(11)
            userrequestdata1 = struct.unpack('!H',userrequestdata[9:11])[0]
            chan1 = userrequestdata1 + 1001

            sock.sendall(userrequestbuf)
            userrequestdata = sock.recv(11)
            userrequestdata2 = struct.unpack('!H',userrequestdata[9:11])[0]
            chan2 = userrequestdata2 + 1001

            pl1 = struct.pack('!HH',userrequestdata1,chan2)
            channelrequestbuf1=channelrequestbuf+pl1
            sock.sendall(channelrequestbuf1)
            res = sock.recv(11)
            if res[7:9] == b"\x3e\x00":
                pl2 = struct.pack('!HH',userrequestdata2,chan2)
                channelrequestbuf2 = channelrequestbuf+pl2
                sock.sendall(channelrequestbuf2)
                msg = 'There is ms12-020 vul on %s' %host
                number = 'v21'
                print(msg)
                sock.close()
                return True,host,number,msg
            else:
                msg = 'There is no ms12-020 vul'
                number = 'v0'
                return False, host,number,msg
        else:
            msg = 'This port isnot rdp protocol'
            print(msg)
            number = 'v0'
            sock.close()
            return False,host,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        sock.close()
        return False,host,number,msg

if __name__ == '__main__':
    res = verify('http','146.196.114.106',3389)
    print(res)