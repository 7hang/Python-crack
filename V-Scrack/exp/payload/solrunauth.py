# coding: utf-8

import sys
import requests
import warnings
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if solr unauth vul')
    warnings.filterwarnings("ignore")
    payload = '/solr/admin/cores?wt=json&indexInfo=false'
    vulnurl = url + payload
    try:
        req = requests.get(vulnurl,timeout=3, verify=False)
        if r"instanceDir" in req.text and r"dataDir" in req.text:
            adminurl = url + '/solr'
            msg = 'There is a solr unauth vul on %s' % adminurl
            print(msg)
            number = 'v26'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url,number,msg
    msg = 'There is no solr uadmin nauth vul'
    number = 'v0'
    return False, url, number, msg