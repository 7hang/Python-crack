# -*- coding:utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import re
import ssl
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def check_zabbix(url):
    url = url + '/index.php'
    if 'http' in url or 'https' in url:
        try:
            h1 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            }
            s = requests.session()
            res = s.get(url, timeout=5, verify=False, headers=h1)
            res_html = res.text
        except requests.HTTPError as e:
            try:
                res_html = e.text
            except Exception:
                res_html = ''
        except Exception as e:
            res_html = ''
        if re.search('www.zabbix.com', res_html, re.I) or re.search('Zabbix SIA', res_html, re.I):
            print("THE url : " + url + " have a service : zabbix .")
            return True
        else:
            return False
    else:
        return False
    return False

def _get_static_post_attr(page_content):
    _dict = {}
    soup = BeautifulSoup(page_content, "html.parser")
    for each in soup.find_all('input'):
        if 'value' in each.attrs and 'name' in each.attrs:
            _dict[each['name']] = each['value']
    return _dict

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if zabbix default password vulnerability')
    url = url + '/zabbix'
    h1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    h2 = {
        'Referer': url.strip('\n'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    blacklist = [
        'incorrect',
        '<!-- Login Form -->',

    ]
    try:
        whetherza = check_zabbix(url)
        print(whetherza)
        if whetherza == True:
            s = requests.session()
            c = s.get(url, timeout=5,verify=False, headers=h1)
            dic = _get_static_post_attr(c.content)
            dic['name'] = 'Admin'
            dic['password'] = 'zabbix'
            dic['enter']='Sign in'
            r = s.post(url + '/index.php', data=dic, headers=h2, verify = False,timeout=5)
            print(r.content)
            if b'chkbxRange.init();' in r.content:
                for each in blacklist:
                    if each in r.content:
                        msg = 'There is no zabbix default password vulnerability'
                        number = 'v0'
                        return False, url, number, msg
                msg = 'Found zabbix default password vulnerability exists at the target address :' + url + ' with user : Admin and passwrd : zabbix. '
                print(msg)
                number = 'v107'
                return True, url, number, msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no zabbix default password vulnerability'
    number = 'v0'
    return False, url, number, msg
