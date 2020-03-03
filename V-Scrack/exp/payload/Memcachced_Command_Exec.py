#-*-coding:utf-8-*-

import re
import telnetlib

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if memcached all version memory injection command execution vul')
    try:
        conn = telnetlib.Telnet(ip, int(port), timeout=3)
        conn.write(b'stats\n')
        regexp = re.compile(b'STAT pid \d+', re.I | re.DOTALL)
        index, _, _ = conn.expect([regexp], timeout=3)
        conn.close()
        if index == 0:
            msg = 'There is memcached all version memory injection command execution vul on url: ' + url + ' .'
            print(msg)
            number = 'v102'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no memcached all version memory injection command execution vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',11211)
    print(res)