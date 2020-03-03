__author__ = '10192989'
# coding:utf-8

import re
import hashlib
import struct
import random
from exp.lib.gla import getpassdict
from exp.lib.gla import str2hex
import pymysql

def get_hash(password, scramble):
    hash_stage1 = hashlib.sha1(password.encode("utf8")).digest()
    hash_stage2 = hashlib.sha1(hash_stage1).digest()
    to = hashlib.sha1(scramble.hex() + hash_stage2).digest()
    reply = [ord(h1) ^ ord(h3) for (h1, h3) in zip(hash_stage1, to)]
    hash = struct.pack('20B', *reply)
    return hash

def get_scramble(packet):
    tmp = packet[15:]
    m = re.findall(b"\x00?([\x01-\x7F]{7,})\x00", tmp)
    #m = re.findall("00?([01-7F]{7,})00", tmp)
    if len(m) > 3: del m[0]
    scramble = m[0] + m[1]
    try:
        plugin = m[2]
    except:
        plugin = ''
    return plugin.hex(), scramble.hex()

def get_auth_data(user, password, scramble, plugin):
    #user_hex = binascii.b2a_hex(user)
    user_hex = str2hex(user)
    #pass_hex = binascii.b2a_hex(get_hash(password, scramble))
    pass_hex = str2hex(get_hash(password, scramble))
    if not password:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0000"
    else:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0014" + pass_hex
    if plugin: data += str2hex(
        plugin) + "0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634"
    len_hex = hex(len(data) / 2).replace("0x", "")
    auth_data = len_hex + "000001" + data
    return str2hex(auth_data)

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if mysql weak pass vul')
    user_list = ['root']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('r00t')
    psw.append('root123')
    psw.append(' ')
    #psw = random.sample(psw, 5)
    for user in user_list:
        for pass_ in psw:
            try:
                if pass_ == ' ':
                    db = pymysql.connect(host=ip, port=int(port), user=user, connect_timeout = 10)
                else:
                    db = pymysql.connect(host=ip, port=int(port), user=user, passwd=pass_, connect_timeout = 10)
                curs = db.cursor()
                curs.close()
                db.close()
                if pass_ == ' ':
                    pass_ = 'None'
                msg = 'There is mysql weak pass vul on: %s , with username: %s and password: %s.' %(url,user,pass_)
                print(msg)
                number = 'v70'
                return True,url,number,msg
            except Exception as e:
                msg = str(e)
                print(msg)
                pass
    msg = 'Therer is no mysql weakpass vul in url:' +url+'.'
    number = 'v0'
    return False,url,number,msg

