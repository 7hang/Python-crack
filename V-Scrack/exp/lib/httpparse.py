# -*- coding:utf-8 -*-

import http.client




class httpparse():
    def __init__(self):
        pass


    def httptest(self,protocol,ip,port,path):
        header={}
        if protocol == 'http':
            url = 'http://'+ip+':'+str(port)+path
            try:
                conn = http.client.HTTPConnection('%s' %ip,str(port),timeout=5)
                conn.request('GET',path,'',headers={})
                a = conn.getresponse()
                #print a.status,a.read()
                return a.status,a.read(),a.getheaders()
            except Exception as e:
                pass

        elif protocol == 'https':
            nurl = 'https://'+ip+':'+str(port)
            try:
                conn = http.client.HTTPSConnection('%s' %ip,str(port),timeout=5)
                conn.request('GET',path,'', headers={})
                a = conn.getresponse()
                return a.status,a.read(),a.getheaders()
            except Exception as e:
                pass



    def httpreq(self,method,protocol,ip,port,path,data='',header={}):
        if protocol == 'http':
            try:
                conn = http.client.HTTPConnection("%s" %ip,str(port),timeout=8)
                if method == 'POST':
                    headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; irai_install; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; irai_install; TCO_20151103165025)",
                               "Accept-Language":"zh-CN","Content-Type":"application/x-www-form-urlencoded",
                               "Content-Length":str(len(data))}
                    headers = dict(headers, **header)
                    conn.request("POST", path, data, headers)
                else:
                    conn.request("GET",path, headers=header)
                response = conn.getresponse()
                return response.status, response.getheaders(), response.read()
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()
        else:
            try:
                conn = http.client.HTTPSConnection("%s" %ip,str(port),timeout=8)
                if method == 'POST':
                    headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; irai_install; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; irai_install; TCO_20151103165025)",
                               "Accept-Language":"zh-CN","Content-Type":"application/x-www-form-urlencoded",
                               "Content-Length":str(len(data))}
                    headers = dict(headers, **header)
                    conn.request("POST", path, data, headers)
                else:
                    conn.request("GET", url=protocol+'://'+ip+':'+str(port)+path, headers=header)
                response = conn.getresponse()
                return response.status, response.getheaders(), response.read()
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()


    def httpreqj(self,method,protocol,ip,port,path,data='',header={}):
        if protocol == 'http':
            try:
                conn = http.client.HTTPConnection("%s" %ip,str(port),timeout=8)
                if method == 'POST':
                    headers = {"Content-Type":"application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue",
                               "Content-Length":str(len(data))}
                    headers = dict(headers, **header)
                    conn.request("POST", path, data, headers)
                else:
                    conn.request("GET",path, headers=header)
                response = conn.getresponse()
                return response.status, response.getheaders(), response.read()
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()
        else:
            try:
                conn = http.client.HTTPSConnection("%s" %ip,str(port),timeout=8)
                if method == 'POST':
                    headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; irai_install; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; irai_install; TCO_20151103165025)",
                               "Accept-Language":"zh-CN","Content-Type":"application/x-www-form-urlencoded",
                               "Content-Length":str(len(data))}
                    headers = dict(headers, **header)
                    conn.request("POST", path, data, headers)
                else:
                    conn.request("GET", url=protocol+'://'+ip+':'+str(port)+path, headers=header)
                response = conn.getresponse()
                return response.status, response.getheaders(), response.read()
            except Exception as e:
                print(e)
            finally:
                if conn:
                    conn.close()


