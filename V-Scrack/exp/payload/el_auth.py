# coding: utf-8

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    vulurl = url +'/_cat'
    try:
        print('testing if Elasticsearch unauth vul')
        res= requests.get(vulurl,verify=False, timeout=3)
        if res.status_code == 200 and '/_cat/master' in res.text:
            msg = 'There is a Elasticsearch unauth vul on %s' %url
            print(msg)
            number = 'v82'
            return True,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no Elasticsearch unauth vul'
    number = 'v0'
    return False,url,number,msg