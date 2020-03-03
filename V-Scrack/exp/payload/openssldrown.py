# -*- coding:utf-8 -*-

import ssl
import socket
import binascii
import codecs


decode_hex = codecs.getdecoder('hex_codec')

def str2hex(x):
    asdad = bytes(x, 'utf-8')
    return asdad.hex()

def h2bin(x):
    return decode_hex(x.replace(' ', '').replace('\n', ''))[0]

def bin2hex(x):
    return ''.join(['%02x' % b for b in x])

def check_tls(host, port):
    client_hello = '16030100d8010000d403037d408377c8e5204623867604ab0ee4a140043a4e383f770a1e6b66c2d45d34e820de8656a211d79fa9809e9ae6404bb7bcc372afcdd6f51882e39ac2241a8535090016c02bc02fc00ac009c013c01400330039002f0035000a0100007500000014001200000f7777772e65746973616c61742e6567ff01000100000a00080006001700180019000b00020100002300003374000000100017001502683208737064792f332e3108687474702f312e31000500050100000000000d001600140401050106010201040305030603020304020202'
    client_hello = binascii.unhexlify(client_hello)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((host, port))
    s.send(client_hello)
    try:
        data = s.recv(1024*1024)
    except socket.timeout:
        data = ''
    except Exception as e:
        print(str(e))

    if data:
        server_hello_len = int(bin2hex(data[3:5]),16)
        index = 5
        index += server_hello_len
        cert_msg = data[index:]

        return cert_msg

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if openssl drown vul')
    client_hello_payload = '803e0100020015001000100100800200800600400400800700c00800800500806161616161616161616161616161616161616161616161616161616161616161'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        port = int(port)
        s.connect((ip, port))
        client_hello_payload = binascii.unhexlify(client_hello_payload)
        s.sendall(client_hello_payload)
        try:
            server_hello = s.recv(10*1024)
        except socket.timeout:
            msg = 'Cannot connect to SSLv2'
            number = 'v0'
            return False,url,number,msg
        except socket.error as e:
            msg = 'Therer is no openssl drown vul'
            number = 'v0'
            return False,url,number,msg
        except Exception as e:
            print(str(e))


        if server_hello:
            try:
                index = 0
                index += 2
                index += 1
                index += 1
                index += 1
                index += 2
                cert_len = int(bin2hex(server_hello[index:index + 2]), 16)
                index += 2
                index += 2
                index += 2
                cert = server_hello[index:cert_len+1]
                data = check_tls(ip,port)
                if data:
                    print(" [*] Check the TLS CERT and SSLv2 CERT")
                    if bin2hex(cert) in bin2hex(data):
                        msg = " [+] SSLv2 Enable - Same cert"
                    else:
                        msg = " [+] SSLv2 Enable - Not same cert"
                    s.close()
                    msg = msg + ".  There is openssl drown vul on url: " + url +" ."
                    number = 'v66'
                    print(msg)
                    return True,url,number,msg
                else:
                    pass
            except Exception as e:
                print(str(e))
                pass
        else:
            pass

    except Exception as e:
        print(str(e))
        pass
    msg = 'There is no openssl drown vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','218.60.28.46',443)
    print(res)