#-*-coding:utf-8-*-

import requests
import ast
import re

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if CVE-2018-1002105 Kubernetes apiserver can leave vulnerable TCP connections vul')
    testkubeurls = '/swagger.json'
    newurl = url + testkubeurls
    try:
        response = requests.get(newurl,verify=False,timeout=3)
        if ('Kubernetes' in response.text and 'api' in response.text) or ('swaggerapi' in response.text and '/api/' in response.text):
            testkube = True
        else:
            testkube = False
        testkubevulurl = '/version'
        newurl02 = url + testkubevulurl
        res = requests.get(newurl02,verify=False, timeout=3)
        resDict = ast.literal_eval(res.text)
        version = resDict["gitVersion"]
        pattern = re.compile(r'\d+.\d+.\d+')
        ver = pattern.findall(version)
        version = [verone.split(".") for verone in ver][0]
        first_two_minor_digists = eval(version[1])
        if first_two_minor_digists < 10:
            testkubevul = True
        else:
            last_two_minor_digists = eval(version[2])
            if first_two_minor_digists == 10 and last_two_minor_digists < 11:
                testkubevul = True
            elif first_two_minor_digists == 11 and last_two_minor_digists < 5:
                testkubevul = True
            elif first_two_minor_digists == 12 and last_two_minor_digists < 3:
                testkubevul = True
        if testkubevul == True and testkube == True:
            msg = 'Found CVE-2018-1002105 Kubernetes apiserver can leave vulnerable TCP connections vul on url: ' + newurl02 + ' .'
            print(msg)
            number = 'v99'
            return True, url, number, msg
        elif testkubevul == True and testkube == False:
            msg = 'Likely found CVE-2018-1002105 Kubernetes apiserver can leave vulnerable TCP connections vul on url: ' + newurl02 + ' . Please check the url whether it is Kubernetes apiserver , if it is not , please send email to 10192989 .'
            print(msg)
            number = 'v99'
            return True, url, number, msg
        elif testkubevul == False:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2018-1002105 Kubernetes apiserver can leave vulnerable TCP connections vul'
    number = 'v0'
    return False, url, number, msg






