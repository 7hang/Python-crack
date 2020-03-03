# coding:utf-8

import requests
import warnings
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if hadoop hdfs unauthorized access vul')
    warnings.filterwarnings("ignore")
    payload = '/dfshealth.html#tab-overview'
    try:
        vulnurl = url + payload
        req = requests.get(url=vulnurl, verify=False, timeout=5)
        if 'active' in req.text and 'files and directories' in req.text and 'Heap Memory used' in req.text:
            msg = 'There is hadoop hdfs unauthorized access vul on url :' + vulnurl + ' .'
            number = 'v122'
            print(msg)
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no hadoop hdfs unauthorized access vul'
    number = 'v0'
    return False, url, number, msg