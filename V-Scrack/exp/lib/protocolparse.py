# -*- coding:utf-8 -*-

import re
import urllib
from exp.lib.httpparse import httpparse
import requests
from exp.lib.gla import gettag
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class protocoparse():
    def __init__(self):
        pass

    @staticmethod
    def judegIp(ip):
        ip = str(ip)
        reg = re.compile(r'\d+\.\d+\.\d+\.\d+[\-\/]?[\d]*')
        try:
            return reg.findall(ip)[0]
        except Exception as e:
            return False

    @staticmethod
    def protocolurlset(ip,port):
        urls = ['websphereconsole|/ibm/console/logon.jsp','weblogicconsole|/console/login/LoginForm.jsp','jbossadmin|/admin-console/index.seam','jbossconsole|/jmx-console/','jbosspass|/web-console/','jboss|/invoker/JMXInvokerServlet']
        http = httpparse()
        ip = protocoparse.judegIp(ip)
        port = int(port)
        try:
            for url in urls:
                path = url.split('|')[1]
                module = url.split('|')[0]
                tm = http.httptest('https','%s' %ip,port,path)
                if tm and (tm != None) and (tm[0] != 404) and (tm[0] != 504) and (tm[0] != 502):
                    protocol = 'https'
                    rip = ip
                    port = str(port)
                    npath = path
                    nmodule = module
                    return protocol,rip,port,npath,nmodule
                else:
                    domain = 'http://'+ip+':'+str(port)
                    tm = http.httptest('http','%s' %ip,port,path)
                    if tm and (tm != None) and (tm[0] != 404) and (tm[0] != 400) and (tm[0] != 504) and (str(tm[2]) != []):
                        protocol = 'http'
                        rip = ip
                        port = str(port)
                        npath = path
                        nmodule = module
                        return protocol,rip,port,npath,nmodule
                    else:
                        pass
            else:
                protocol = ''
                rip = ip
                port = str(port)
                npath = ''
                nmodule = ''
                return protocol,rip,port,npath,nmodule
        except Exception as e:
            print(e)


    @staticmethod
    def protocolset(ip,port):
        http = httpparse()
        ip = protocoparse.judegIp(ip)
        path = ''
        port = str(port)
        try:
            tm = http.httptest('http','%s' %ip, port,path)
            if tm and (tm != None) and (tm[0] != 504) and (tm[0] != 400) and (tm[0] != 502) and (str(tm[2]) != []):
                protocol = 'http'
                rip = ip
                port = str(port)
                return protocol,rip,port
            else:
                tms = http.httptest('https', '%s' %ip, port,path)
                if tms and (tms != None) and (tms[0] != 504) and (tms[0] != 502):
                    protocol = 'https'
                    rip = ip
                    port = str(port)
                    return protocol,rip,port
                else:
                    if tm and (tm != None) and tm[0] == 400:
                        protocol = 'http'
                        rip = ip
                        port = str(port)
                        return protocol,rip,port
                    else:
                        protocol = ''
                        rip = ip
                        port = str(port)
                        return protocol,rip,port
        except Exception as e:
            print(e)

    @staticmethod
    def servicetest(ip,port,protocol_name,service_name):
        protocol = ''
        file_tmp = {}
        if protocol_name in ['postgresql','memcached','telnet','ftp','mongod','mysql','ssh','java-rmi','ms-wbt-server','ms-sql-s','redis','smtp','rtsp']:
            tag = protocol_name
            print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
            return tag,protocol
        elif int(port) == 161:
            tag = 'snmp'
            print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
            return tag, protocol
        elif int(port) == 445:
            tag = 'smb'
            print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
            return tag, protocol
        elif int(port) == 873:
            tag = 'rsync'
            print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
            return tag, protocol
        elif int(port) == 25:
            tag = 'smtp'
            print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
            return tag, protocol
        elif int(port) == 11211:
            tag = 'memcached'
            print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
            return tag, protocol
        else:
            (protocol,ip,port) = protocoparse.protocolset(ip,port)
            if protocol == 'http' or protocol == 'https':
                if int(port) == 9200:
                    tag = 'elsearch'
                    print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                    return tag,protocol
                elif int(port) == 3000:
                    tag = 'grafan'
                    print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                    return tag,protocol
                elif int(port) == 50070:
                    tag = 'hdfs'
                    print("THE ip " + ip + ":" + str(port) + " have a service : " + tag + ' .')
                    return tag, protocol
                else:
                    pass
            if protocol == 'http' or protocol == 'https':
                url = protocol + '://'+ip+':'+str(port)
                try:
                    res = requests.get(url,verify=False,timeout=5)
                    res_header = res.headers
                    res_html = res.text

                except requests.HTTPError as e:
                    try:
                        res_header = e.headers

                    except Exception:
                        res_header = ''
                    try:

                        res_html = e.text
                    except Exception:
                        res_html = ''
                except Exception as e:
                    res_html = ''
                    res_header = ''
                tags = gettag()
                marks = tags.get_tag()
                for mark in marks:
                    markinfo = mark.strip().split("|",3)
                    if markinfo[1] == 'header':
                        try:
                            if res_header == '':
                                tag = 'None'
                                print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                                return tag,protocol
                            if re.search(markinfo[3],res_header[markinfo[2]], re.I):
                                tag = markinfo[0]
                                print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                                return tag,protocol
                        except Exception as e:
                            continue
                    elif markinfo[1] == 'file':
                        if markinfo[2] == 'index':
                            try:
                                if re.search(markinfo[3],res_html, re.I):
                                    tag = markinfo[0]
                                    print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                                    return tag,protocol
                            except Exception as e:
                                continue
                        else:
                            if markinfo[2] in file_tmp:
                                re_html = file_tmp[markinfo[2]]
                            else:
                                try:
                                    re_html = urllib.request.urlopen(url + "/" + markinfo[2],timeout=5).read().decode('utf-8','ignore')
                                except urllib.error.HTTPError as e:
                                    try:
                                        re_html = e.read().decode('utf-8','ignore')
                                    except Exception as e:
                                        re_html = ''
                                except Exception as e:
                                    continue
                                    #tag = 'None'
                                    #print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                                    #return tag,protocol
                                file_tmp[markinfo[2]] = re_html
                            try:
                                if re.search(markinfo[3], re_html, re.I):
                                    tag = markinfo[0]
                                    print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
                                    return tag,protocol
                            except Exception as e:
                                continue
            else:
                pass
        tag = 'None'
        print("THE ip "+ip+":"+str(port)+" have a service : " + tag+' .')
        return tag,protocol
