__author__ = '10192989'
# coding:utf-8

from urllib.parse import urljoin
from xml.dom import minidom
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scan(site, headers_fake):
    rnt = {'status': 'noxml',
           'site': site}
    crossdoman_url = urljoin(site, '/crossdomain.xml')
    try:
        resp = requests.get(crossdoman_url,headers=headers_fake,verify=False,timeout=3)
        html = resp.text
        if not html:
            return rnt
        if not '<cross-domain-policy' in resp:
            return rnt
        rnt['status'] = 'nocsrf'
        try:
            xmldom = minidom.parseString(resp)
            for o in xmldom.getElementsByTagName('allow-access-from'):
                domain = o.getAttribute('domain').strip()
                if domain == '*':
                    rnt['status'] = 'csrf'
                    return rnt
        except Exception as e:
            msg = str(e)
            print(msg)
            pass
    except Exception as e:
        msg = str(e)
        print(msg)
        pass
    return rnt

def verify(protocol,ip,port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if flash crossdomain.xml cross site request forgery vul')
    human_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
        'Accept-Encoding': 'gzip,deflate,sdch'
    }
    try:
        r = scan(url, human_headers)
        if r['status'] == 'csrf':
            msg = 'Found flash crossdomain.xml cross site request forgery vul in url:' + url + '/crossdomain.xml .'
            print(msg)
            number = 'v102'
            return True, url, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg
    msg = 'There is no flash crossdomain.xml cross site request forgery vul'
    number = 'v0'
    return False, url, number, msg






