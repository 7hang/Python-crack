# -*- coding:utf-8 -*-

from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if jenkins unauth vul')
    http = httpparse()
    try:
        path = ''
        tm = http.httpreq('GET', protocol, ip, port, path)
        if tm and (tm != None) and tm[0] == 200 and b'/asynchPeople/' in tm[2] :
            path = path+'/script'
            print(path)
            newtm = http.httpreq('GET', protocol, ip, port, path)
            if newtm and (newtm != None) and newtm[0] == 200 and b'println' in newtm[2] and b'submit' in newtm[2]:
                msg = 'There is a jenkins unauth vul which can result in get shell on %s' %url
                print(msg)
                number = 'v36'
                return True,url,number,msg
            else:
                pass
        else:
            pass
        url = protocol+'://'+ip+':'+str(port)
        path = '/jenkins/'
        tm1 = http.httpreq('GET', protocol, ip, port, path)
        if tm1 and (tm1 != None) and tm1[0] == 200 and b'Dashboard [Jenkins]' in tm1[2] :
            path = path+'/script'
            newtm1 = http.httpreq('GET', protocol, ip, port, path)
            if newtm1 and (newtm1 != None) and newtm1[0] == 200 and b'println' in newtm1[2] and b'submit' in newtm1[2]:
                msg = 'There is a jenkins unauth vul which can result in get shell on %s' %url
                print(msg)
                number = 'v36'
                return True,url,number,msg
            else:
                pass
        else:
            pass
    except Exception as e:
        print(str(e))
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'There is no jenkins unauth vul'
    number = 'v0'
    return False,url,number,msg
